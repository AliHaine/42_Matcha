from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from database import connectDatabase, createTables, createElem, getElems, deleteElem, modifyElem
from models import User, create_user, ALLOWED_CHARACTERS, PASSWORD_REQUIREMENTS, REQUIRED_FIELDS, login_user_func, UserInterests, interests, init_interests, modifyUserInterest, getAllUsersInterest, LIST_INTERESTS
from crypting import init_bcrypt

app = Flask(__name__)
app.secret_key = "super secret key"


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

@app.route('/api/test', methods=['GET'])
def test():
    if userIsLoggedIn() == True:
        getAllUsersInterest(session.get('email'))
    return jsonify({'Success': 'Test success'})

@app.route('/api/register', methods=['POST'])
def register_user():
    values = request.json
    if userIsLoggedIn() == True:
        return jsonify({'Error': 'User already logged in'})
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
            return jsonify({'Error': f'Missing required field: {field}'})
    try:
        create_user(user)
        login_user_func(user)
        return jsonify({'Success': 'User created successfully'})
    except Exception as e:
        return jsonify({'Error': str(e)})

@app.route('/api/registerRequirements', methods=['GET'])
def get_register_requirements():
    # return ALLOWED_CHARACTERS, PASSWORD_REQUIREMENTS
    return jsonify({'allowed_charactes': ALLOWED_CHARACTERS, 'password_requirements': PASSWORD_REQUIREMENTS, 'required fields': REQUIRED_FIELDS + ['passwordConfirm']})

@app.route('/api/login', methods=['POST'])
def loginRoute():
    data = request.json
    if userIsLoggedIn() == True:
        return jsonify({'Error': 'User already logged in'})
    email = data.get('email', '')
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'Error': 'Missing required fields'})
    try:
        user = {
            'email': email,
            'password': password
        }
        login_user_func(user)
        return jsonify({'Success': 'User logged in successfully'})
    except Exception as e:
        return jsonify({'Error': str(e)})
    
@app.route('/api/logout', methods=['GET'])
def logoutRoute():
    if userIsLoggedIn() == False:
        return jsonify({'Error': 'User already logged out'})
    if session.get('email'):
        session.pop('email')
        return jsonify({'Success': 'User logged out successfully'})
    return jsonify({'Error': 'User not logged in'})

@app.route('/api/modifyDescription', methods=['POST'])
def modifyDescription():
    data = request.json
    if userIsLoggedIn() == False:
        return jsonify({'Error': 'you must be logged in to modify description'})
    description = data.get('description', '')
    if len(description) <= 0:
        return jsonify({'Error': 'you must provide a description'})
    user = getElems(User, {'email': session.get('email')})[0]
    try:
        modifyElem(User, user[0], {'description': description})
        return jsonify({'Success': 'Description updated successfully'})
    except Exception as e:
        return jsonify({'Error': str(e)})

    
    
@app.route('/api/modifyInterests', methods=['POST'])
def addInterests():
    data = request.json
    if userIsLoggedIn() == False:
        return jsonify({'Error': 'you must be logged in to modify interests'})
    interests = data.get('interests', [])
    # if len(interests) < 3:
    #     return jsonify({'Error': 'not enough interests provided'})
    user = getElems(User, {'email': session.get('email')})[0]
    deleteElem(UserInterests, {'user_id': user[0]})
    if len(interests) > 0:
        for interest in interests:
            print(interest)
            try:
                modifyUserInterest(session.get('email'), interest)
                pass
            except Exception as e:
                return jsonify({'Error': str(e)})
    return jsonify({'Success': 'Interests added successfully'})

@app.route('/api/getInterests', methods=['GET'])
def getGlobalInterests():
    return jsonify({'interests': LIST_INTERESTS})
    

if __name__ == '__main__':
    connectDatabase()
    tupleModels = (User, interests, UserInterests)
    createTables(tupleModels)
    init_bcrypt(app)
    init_interests()
    app.run(debug=True, host='localhost', port=8000)
