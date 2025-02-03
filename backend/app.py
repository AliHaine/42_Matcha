from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from database import connectDatabase, createTables, getElems, deleteElem, modifyElem, dropAll, databaseConnected, createElem
from models import *
from crypting import init_bcrypt
import sys
from config import *
from algo import *
import os
import requests
from PIL import Image

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = BASE_DIR + '/media'
app.config['PROFILE_PIC_FOLDER'] = BASE_DIR + '/media/profile_pics'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config["SESSION_COOKIE_SAMESITE"] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = False


CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"]}}, supports_credentials=True)

def find_files_with_prefix(directory, prefix):
    return [
        file for file in os.listdir(directory)
        if file.startswith(prefix)
    ]

def userIsLoggedIn():
    sessionEmail = session.get('email')
    print(sessionEmail)
    users = getElems(User, {'email': sessionEmail})
    print(users)
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
        if not user[USER_ENUM['firstname']] or not user[USER_ENUM['lastname']] or not user[USER_ENUM['email']] or not user[USER_ENUM['age']] or not user[USER_ENUM['sex']]:
            ret['Success'] = False
            ret['Errors'].append('Missing mandatory fields')
            ret['Missings'].append("mandatory")
        if not user[USER_ENUM['description']]:
            ret['Success'] = False
            ret['Errors'].append('Missing description')
            ret['Missings'].append("description")
        if not user[USER_ENUM['weight']] or not user[USER_ENUM['height']] or not user[USER_ENUM['corpu']]:
            ret['Success'] = False
            ret['Errors'].append('Missing body info')
            ret['Missings'].append("body")
        if user[USER_ENUM['smoking']] is None or not user[USER_ENUM['drink']] or not user[USER_ENUM['diet']]:
            ret['Success'] = False
            ret['Errors'].append('Missing health info')
            ret['Missings'].append("health")
        if not user[USER_ENUM['research']] or not user[USER_ENUM['engagement']] or not user[USER_ENUM['frequency']]:
            ret['Success'] = False
            ret['Errors'].append('Missing looking for info')
            ret['Missings'].append("lookingFor")
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
        'firstname': values.get('firstname', ''),
        'lastname': values.get('lastname', ''),
        'email': values.get('email', ''),
        'password': values.get('password', ''),
        'passwordConfirm': values.get('passwordConfirm', ''),
        'age': values.get('age', ''),
        'sex': values.get('sex', ''),
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
        retMissingFields = checkMissingFields(session.get('email'))
        if retMissingFields['Success'] == False:
            return jsonify(retMissingFields)
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
        'firstname': data.get('firstname', None),
        'lastname': data.get('lastname', None),
        'age': data.get('age', None),
        'sex': data.get('sex', None),
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
        'firstname': user[USER_ENUM['firstname']],
        'lastname': user[USER_ENUM['lastname']],
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
    smoking = data.get('smoking', None)
    drink = data.get('drink', None)
    diet = data.get('diet', None)
    if not drink or not diet or smoking is None:
        return jsonify({'Success': False, 'Error': 'you must provide all the sanity fields (fumeur, boit, alimentation)'})
    sanity = {
        'smoking': smoking,
        'drink': drink,
        'diet': diet
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
    height = data.get('height', None)
    weight = data.get('weight', None)
    corpu = data.get('corpu', None)
    if not height or not weight or not corpu:
        return jsonify({'Success': False, 'Error': 'you must provide all the body info fields (height, weight, corpu)'})
    user = getElems(User, {'email': session.get('email')})[0]
    bodyInfo= {
        'height': height,
        'weight': weight,
        'corpu': corpu
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
    research = data.get('research', None)
    engagement = data.get('engagement', None)
    frequency = data.get('frequency', None)
    if not research or not engagement or not frequency:
        return jsonify({'Success': False, 'Error': 'you must provide all the ideal Relation fields (research, engagement, frequency)'})
    user = getElems(User, {'email': session.get('email')})[0]
    idealRelation = {
        'research': research,
        'engagement': engagement,
        'frequency': frequency
    }
    try:
        modifyUserIdealRelation(idealRelation, user[0])
        print("\n\n\n\nsession", session)
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
    return jsonify({'sanity': ['smoking', 'drink', 'diet'],
                    'smoking': [True, False],
                    'drink': LIST_DRINK,
                    'diet': LIST_DIET})

@app.route('/api/getBodyInfo', methods=['GET'])
def getBodyInfoRoute():
    return jsonify({'body_info': ['height', 'weight', 'corpu'],
                    'hieght': {'min': MIN_HEIGHT, 'max': MAX_HEIGHT},
                    'weight': {'min': MIN_WEIGHT, 'max': MAX_WEIGHT},
                    'corpu': LIST_CORPU})

@app.route('/api/getIdealRelation', methods=['GET'])
def getIdealRelationRoute():
    return jsonify({'ideal_relation': ['research', 'engagement', 'frequency'],
                    'research': LIST_RESEARCH,
                    'engagement': LIST_ENGAGEMENT,
                    'frequency': LIST_FREQUENCY})

@app.route('/api/account/profiles/<int:page>', methods=['GET'])
def getProfilesRoute(page):
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to get profiles'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
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
    nbProfiles = request.args.get('nbProfiles', default=8, type=int)
    user = getElems(User, {'email': session.get('email')})[0]
    matcha = getMatchableUsers(user[0], nbProfiles)
    return jsonify({'Success': True, 'matcha': matcha})

@app.route('/api/account/setLocation', methods=['POST'])
def getLocationRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to set location'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    user = getElems(User, {'email': session.get('email')})[0]
    lon = request.args.get('lon', None)
    lat = request.args.get('lat', None)
    if not lon or not lat:
        return jsonify({'Success': False, 'Error': 'You must provide lon and lat'})
    if type(lon) == str:
        try:
            lon = float(lon)
        except:
            return jsonify({'Success': False, 'Error': 'lon must be a float'})
    if type(lat) == str:
        try:
            lat = float(lat)
        except:
            return jsonify({'Success': False, 'Error': 'lat must be a float'})
    if type(lon) != float or type(lat) != float:
        return jsonify({'Success': False, 'Error': 'lon and lat must be floats'})
    try:
        res = requests.get(f'https://geo.api.gouv.fr/communes?lat={lat}&lon={lon}&fields=code,nom,departement,region')
        if res.status_code != 200:
            return jsonify({'Success': False, 'Error': 'Invalid location'})
        data = res.json()
        if len(data) == 0:
            return jsonify({'Success': False, 'Error': 'Invalid location'})
        city = data[0]
        if city is None:
            return jsonify({'Success': False, 'Error': 'Invalid location'})
        cityID = checkCity(city)
        if cityID is None:
            return jsonify({'Success': False, 'Error': 'Invalid location'})
        userCity = getElems(UserCity, {'user_id': user[USER_ENUM['id']]})
        if len(userCity) == 0:
            print("create")
            createElem(UserCity, {'user_id': user[USER_ENUM['id']], 'city_id': cityID}, ['user_id', 'city_id'])
        else:
            print("modify")
            modifyElem(UserCity, userCity[0][0], {'city_id': cityID})
        return jsonify({'Success': True})
    except Exception as e:
        print("error : ", e)
        return jsonify({'Success': False, 'Error': 'Invalid location'})

@app.route('/api/profile_pics/<path:filename>', methods=['GET'])
def getProfilePicRoute(filename):
    return send_from_directory(app.config['PROFILE_PIC_FOLDER'], filename)

def is_image_corrupted(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Vérifie l'intégrité du fichier
        return False
    except (IOError, SyntaxError):
        return True  # L'image est corrompue

@app.route('/api/account/uploadProfilePic', methods=['POST'])
def uploadProfilePicRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to upload a profile pic'})
    if 'file' not in request.files:
        return jsonify({'Success': False, 'Error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'Success': False, 'Error': 'No selected file'})
    if file and file.filename.split('.')[-1] in app.config['ALLOWED_EXTENSIONS']:
        user = getElems(User, {'email': session.get('email')})[0]
        if (user[USER_ENUM['numberPhoto']] >= 5):
            return jsonify({'Success': False, 'Error': 'You can only upload 5 photos'})
        for i in range(0, 5):
            print("index", i)
            ret = find_files_with_prefix(app.config['PROFILE_PIC_FOLDER'], f"{user[USER_ENUM['id']]}_{i}")
            if len(ret) == 0:
                filename = f"{user[USER_ENUM['id']]}_{i}." + file.filename.split('.')[-1]
                break
        file.save(f"{app.config['PROFILE_PIC_FOLDER']}/{filename}")
        if is_image_corrupted(f"{app.config['PROFILE_PIC_FOLDER']}/{filename}"):
            os.remove(f"{app.config['PROFILE_PIC_FOLDER']}/{filename}")
            return jsonify({'Success': False, 'Error': 'File corrupted'})
        modifyElem(User, user[0], {'numberPhoto': user[USER_ENUM['numberPhoto']] + 1})
        return jsonify({'Success': True})
    return jsonify({'Success': False, 'Error': 'File not allowed'})

def realignPhotos(user_id, photoNumber, numberPhoto):
    for i in range(photoNumber, numberPhoto):
        ret = find_files_with_prefix(app.config['PROFILE_PIC_FOLDER'], f"{user_id}_{i + 1}")
        if len(ret) == 0:
            return
        os.rename(f"{app.config['PROFILE_PIC_FOLDER']}/{ret[0]}", f"{app.config['PROFILE_PIC_FOLDER']}/{user_id}_{i}.{ret[0].split('.')[-1]}")

@app.route('/api/account/deleteProfilePic', methods=['POST'])
def deleteProfilePicRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Success': False, 'Error': 'you must be logged in to delete a profile pic'})
    retMissingFields = checkMissingFields(session.get('email'))
    if retMissingFields['Success'] == False:
        return jsonify(retMissingFields)
    user = getElems(User, {'email': session.get('email')})[0]
    if (user[USER_ENUM['numberPhoto']] <= 0):
        return jsonify({'Success': False, 'Error': 'You must have at least one photo'})
    photoNumber = request.args.get('photoNumber', None)
    if not photoNumber:
        return jsonify({'Success': False, 'Error': 'You must provide a photo number'})
    if type(photoNumber) == str:
        try:
            photoNumber = int(photoNumber)
        except:
            return jsonify({'Success': False, 'Error': 'Photo number must be an integer'})
    if type(photoNumber) != int:
        return jsonify({'Success': False, 'Error': 'Photo number must be an integer'})
    if photoNumber < 0 or photoNumber >= user[USER_ENUM['numberPhoto']]:
        return jsonify({'Success': False, 'Error': 'Photo number out of range'})
    ret = find_files_with_prefix(app.config['PROFILE_PIC_FOLDER'], f"{user[USER_ENUM['id']]}_{photoNumber}")
    if len(ret) == 0:
        return jsonify({'Success': False, 'Error': 'Photo not found'})
    os.remove(f"{app.config['PROFILE_PIC_FOLDER']}/{ret[0]}")
    if photoNumber < user[USER_ENUM['numberPhoto']]:
        realignPhotos(user[USER_ENUM['id']], photoNumber, user[USER_ENUM['numberPhoto']])
    modifyElem(User, user[0], {'numberPhoto': user[USER_ENUM['numberPhoto']] - 1})
    return jsonify({'Success': True})

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
    print(BASE_DIR)
    app.run(debug=True, host='localhost', port=5000)
