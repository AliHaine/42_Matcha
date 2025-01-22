from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from database import connectDatabase, createTables, getElems, deleteElem, modifyElem, dropAll, databaseConnected
from models import *
from crypting import init_bcrypt
import sys
from config import *
from algo import *

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = 'media'
app.config['PROFILE_PIC_FOLDER'] = 'media/profile_pics'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

CORS(app)


def userIsLoggedIn():
    sessionEmail = session.get('email')
    users = getElems(User, {'email': sessionEmail})
    if len(users) == 0 and sessionEmail:
        session.pop('email')
        sessionEmail = None
    if sessionEmail:
        return True
    return False

def checkMissingFields(email):
    users = getElems(User, {'email': email})
    if len(users) == 0 and email:
        session.pop('email')
        email = None
    if email:
        user = users[0]
        ret = {
            "Success": True,
            "Errors": [],
            "Missings": []
        }
        print(user)
        if not user[USER_ENUM['firstName']] or not user[USER_ENUM['lastName']] or not user[USER_ENUM['email']] or not user[USER_ENUM['age']] or not user[USER_ENUM['sexe']]:
            ret['Success'] = False
            ret['Errors'].append('Missing mandatory fields')
            ret['Missings'].append("mandatory")
        if not user[USER_ENUM['description']]:
            ret['Success'] = False
            ret['Errors'].append('Missing description')
            ret['Missings'].append("description")
        if not user[USER_ENUM['poids']] or not user[USER_ENUM['taille']] or not user[USER_ENUM['corpulence']]:
            ret['Success'] = False
            ret['Errors'].append('Missing body info')
            ret['Missings'].append("body")
        if user[USER_ENUM['fumeur']] is None or not user[USER_ENUM['boit']] or not user[USER_ENUM['alimentation']]:
            ret['Success'] = False
            ret['Errors'].append('Missing sanity info')
            ret['Missings'].append("sanity")
        if not user[USER_ENUM['recherche']] or not user[USER_ENUM['engagement']] or not user[USER_ENUM['frequence']]:
            ret['Success'] = False
            ret['Errors'].append('Missing ideal Relation info')
            ret['Missings'].append("ideal")
        return ret
    else:
        return jsonify({'Success': False, 'Error': 'User not found'})


@app.route('/api/test', methods=['GET'])
def testRoute():
    return jsonify({'Success': True})

@app.route('/api/account/checkMissingFields', methods=['GET'])
def checkMissingFieldsRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'User not logged in'})
    return jsonify(checkMissingFields(session.get('email')))

@app.route('/api/account/register', methods=['POST'])
def registerUserRoute():
    values = request.json
    if userIsLoggedIn() == True:
        return jsonify({'Success': False, 'Error': 'User already logged in'})
    user = {
        'firstName': values.get('firstName', ''),
        'lastName': values.get('lastName', ''),
        'email': values.get('email', ''),
        'password': values.get('password', ''),
        'passwordConfirm': values.get('passwordConfirm', ''),
        'age': values.get('age', ''),
        'sexe': values.get('sexe', ''),
    }
    for field in REQUIRED_FIELDS + ['passwordConfirm']:
        if not user.get(field):
            return jsonify({'Success': False, 'Error': f'Missing required field: {field}'})
    try:
        create_user(user)
        login_user_func(user)
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False, 'Error': str(e)})

@app.route('/api/account/login', methods=['POST'])
def loginRoute():
    data = request.json
    if userIsLoggedIn() == True:
        return jsonify({'Success': False, 'Error': 'User already logged in'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    email = data.get('email', '')
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'Success': False, 'Error': 'Missing required field: email or password'})
    try:
        user = {
            'email': email,
            'password': password
        }
        login_user_func(user)
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False, 'Error': str(e)})
    
@app.route('/api/account/logout', methods=['GET'])
def logoutRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'User not logged in'})
    if session.get('email'):
        session.pop('email')
        return jsonify({'Success': True})
    return jsonify({'Success': False, 'Error': 'User not logged in'})

@app.route('/api/account/modifyPersonnalInfo', methods=['POST'])
def modifyPersonnalInfoRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'User not logged in'})
    retMissingFields = checkMissingFields()
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    data = request.json
    userPersonalInfo = {
        'firstName': data.get('firstName', None),
        'lastName': data.get('lastName', None),
        'age': data.get('age', None),
        'sexe': data.get('sexe', None),
        'email': data.get('email', None),
        'password': data.get('password', None),
        'newPassword': data.get('newPassword', None),
        'newPasswordConfirm': data.get('newPasswordConfirm', None)
    }
    for field, value in userPersonalInfo.items():
        if value == "":
            userPersonalInfo[field] = None
    try:
        user = getElems(User, {'email': session.get('email')})[0]
        print(userPersonalInfo)
        modifyUserPersonnalInfo(userPersonalInfo, user[0])
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False, 'Error': str(e)})


@app.route('/api/account/getUser', methods=['GET'])
def getUserRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False,'Error': 'User not logged in'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    user = getElems(User, {'email': session.get('email')})[0]
    return jsonify({'Success': True, 'user': {
        'firstName': user[USER_ENUM['firstName']],
        'lastName': user[USER_ENUM['lastName']],
        'email': user[USER_ENUM['email']],
        'description': user[USER_ENUM['description']]
    }})

@app.route('/api/account/modifyDescription', methods=['POST'])
def modifyDescriptionRoute():
    data = request.json
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to modify description'})
    description = data.get('description', '')
    if len(description) <= 0:
        return jsonify({'Success': False, 'Error': 'you must provide a description'})
    user = getElems(User, {'email': session.get('email')})[0]
    if len(description) > 500:
        return jsonify({'Success': False, 'Error': 'description must be less than 500 characters'})
    try:
        modifyElem(User, user[0], {'description': description})
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False, 'Error': str(e)})
    
@app.route('/api/account/modifyInterests', methods=['POST'])
def modifyInterestsRoute():
    data = request.json
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to modify interests'})
    interests = data.get('interests', [])
    user = getElems(User, {'email': session.get('email')})[0]
    if len(interests) <= 0:
        return jsonify({'Success': False, 'Error': 'you must provide at least one interest'})
    else:
        for interest in interests:
            if interest not in LIST_INTERESTS:
                return jsonify({'Success': False, 'Error': f'Interest {interest} not allowed'})
    deleteElem(UserInterests, {'user_id': user[0]})
    if len(interests) > 0:
        for interest in interests:
            try:
                modifyUserInterest(session.get('email'), interest)
                pass
            except Exception as e:
                return jsonify({'Success': False, 'Error': str(e)})
    return jsonify({'Success': True})

@app.route('/api/account/modifySanity', methods=['POST'])
def modifySanityRoute():
    data = request.json
    if userIsLoggedIn() == False:
        return jsonify({'Success': False,'Error': 'you must be logged in to modify sanity'})
    fumeur = data.get('fumeur', None)
    boit = data.get('boit', None)
    alimentation = data.get('alimentation', None)
    if not boit or not alimentation or fumeur is None:
        return jsonify({'Success': False, 'Error': 'you must provide all the sanity fields (fumeur, boit, alimentation)'})
    sanity = {
        'fumeur': fumeur,
        'boit': boit,
        'alimentation': alimentation
    }
    user = getElems(User, {'email': session.get('email')})[0]
    try:
        checkSanity(sanity, user[0])
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False,'Error': str(e)})

@app.route('/api/account/modifyBodyInfo', methods=['POST'])
def modifyBodyInfoRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to modify body info'})
    data = request.json
    taille = data.get('taille', None)
    poids = data.get('poids', None)
    corpulence = data.get('corpulence', None)
    if not taille or not poids or not corpulence:
        return jsonify({'Success': False, 'Error': 'you must provide all the body info fields (taille, poids, corpulence)'})
    user = getElems(User, {'email': session.get('email')})[0]
    bodyInfo= {
        'taille': taille,
        'poids': poids,
        'corpulence': corpulence
    }
    try:
        modifyUserBody(bodyInfo, user[0])
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False, 'Error': str(e)})

@app.route('/api/account/modifyIdealRelation', methods=['POST'])
def modifyIdealRelationRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to modify ideal Relation'})
    data = request.json
    recherche = data.get('recherche', None)
    engagement = data.get('engagement', None)
    frequence = data.get('frequence', None)
    if not recherche or not engagement or not frequence:
        return jsonify({'Success': False, 'Error': 'you must provide all the ideal Relation fields (recherche, engagement, frequence)'})
    user = getElems(User, {'email': session.get('email')})[0]
    idealRelation = {
        'recherche': recherche,
        'engagement': engagement,
        'frequence': frequence
    }
    try:
        modifyUserIdealRelation(idealRelation, user[0])
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Success': False, 'Error': str(e)})
    

@app.route('/api/registerRequirements', methods=['GET'])
def getRegisterRequirementsRoute():
    # return ALLOWED_CHARACTERS, PASSWORD_REQUIREMENTS
    return jsonify({'allowed_charactes': ALLOWED_CHARACTERS, 'password_requirements': PASSWORD_REQUIREMENTS, 'required fields': REQUIRED_FIELDS + ['passwordConfirm']})

@app.route('/api/getInterests', methods=['GET'])
def getInterestsRoute():
    return jsonify({'interests': LIST_INTERESTS})

@app.route('/api/getSanity', methods=['GET'])
def getSanityRoute():
    return jsonify({'sanity': ['fumeur', 'boit', 'alimentation'],
                    'fumeur': [True, False],
                    'boit': LIST_BOIT,
                    'alimentation': LIST_ALIM})

@app.route('/api/getBodyInfo', methods=['GET'])
def getBodyInfoRoute():
    return jsonify({'body_info': ['taille', 'poids', 'corpulence'],
                    'taille': {'min': MIN_TAILLE, 'max': MAX_TAILLE},
                    'poids': {'min': MIN_POIDS, 'max': MAX_POIDS},
                    'corpulence': LIST_CORPU})

@app.route('/api/getIdealRelation', methods=['GET'])
def getIdealRelationRoute():
    return jsonify({'ideal_relation': ['recherche', 'engagement', 'frequence'],
                    'recherche': LIST_RECHERCHE,
                    'engagement': LIST_ENGAGEMENT,
                    'frequence': LIST_FREQUENCE})

@app.route('/api/account/profiles/<int:page>', methods=['GET'])
def getProfilesRoute(page):
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to get profiles'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    user = getElems(User, {'email': session.get('email')})[0]
    if type(page) != int:
        return jsonify({'Success': False, 'Error': 'Page must be an integer'})
    if page < 1:
        return jsonify({'Success': False, 'Error': 'Page must be greater than 0'})
    profile = getPublicProfile(page)
    return jsonify({'Success': True, 'profile': profile})

@app.route('/api/matcha', methods=['GET'])
def getMatchaRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to get matcha'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    nbProfiles = request.args.get('nbProfiles', default=8, type=int)  # Récupère 'page', avec une valeur par défaut
    user = getElems(User, {'email': session.get('email')})[0]
    matcha = getMatchableUsers(user[0], nbProfiles)
    return jsonify({'Success': True, 'matcha': matcha})

@app.route('/api/account/location', methods=['GET'])
def getLocationRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to get location'})

@app.route('/api/profile_pics/<path:filename>', methods=['GET'])
def getProfilePicRoute(filename):
    return send_from_directory(app.config['PROFILE_PIC_FOLDER'], filename)

@app.route('/api/account/uploadProfilePic', methods=['POST'])
def uploadProfilePicRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to upload a profile pic'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    if 'file' not in request.files:
        return jsonify({'Success': False, 'Error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'Success': False, 'Error': 'No selected file'})
    if file and file.filename.split('.')[-1] in app.config['ALLOWED_EXTENSIONS']:
        user = getElems(User, {'email': session.get('email')})[0]
        filename = f"{user[USER_ENUM['id']]}_" + file.filename
        file.save(f"{app.config['PROFILE_PIC_FOLDER']}/{filename}")
        return jsonify({'Success': True})
    return jsonify({'Success': False, 'Error': 'File not allowed'})

if __name__ == '__main__':
    connectDatabase()
    if databaseConnected() == False:
        print("Error: Database not connected")
        exit(1)
    if len(sys.argv) > 1:
        if sys.argv[1] == "RESET":
            dropAll()
    tupleModels = (User, interests, UserInterests, cities, UserCity)
    createTables(tupleModels)
    init_bcrypt(app)
    init_interests()
    app.run(debug=True, host='localhost', port=8000)
