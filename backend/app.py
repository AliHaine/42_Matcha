from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from database import connectDatabase, createTables, createElem, getElems
from models.user import User, create_user, ALLOWED_CHARACTERS, PASSWORD_REQUIREMENTS, login_user_func
from crypting import init_bcrypt

app = Flask(__name__)
app.secret_key = "super secret key"


CORS(app)

def userIsLoggedIn():
    return session.get('email') is not None

@app.route('/api/register', methods=['POST'])
def register_user():
    values = request.json
    if userIsLoggedIn() == True:
        return jsonify({'Error': 'User already logged in'})
    firstName = values.get('firstName', '')
    lastName = values.get('lastName', '')
    email = values.get('email', '')
    password = values.get('password', '')
    passwordConfirm = values.get('passwordConfirm', '')
    user = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'password': password,
        'passwordConfirm': passwordConfirm
    }
    if not firstName or not lastName or not email or not password or not passwordConfirm:
        return jsonify({'Error': 'Missing required fields'})
    try:
        create_user(user)
        login_user_func(request, user)
        return jsonify({'Success': 'User created successfully'})
    except Exception as e:
        return jsonify({'Error': str(e)})

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
        login_user_func(request, user)
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

@app.route('/api/registerRequirements', methods=['GET'])
def get_register_requirements():
    # return ALLOWED_CHARACTERS, PASSWORD_REQUIREMENTS
    return jsonify({'allowed_charactes': ALLOWED_CHARACTERS, 'password_requirements': PASSWORD_REQUIREMENTS, 'required fields': ['firstName', 'lastName', 'email', 'password', 'passwordConfirm']})

@app.route('/api/addDescription', methods=['POST'])
def addDescription():
    data = request.json
    if userIsLoggedIn() == False:
        return jsonify({'Error': 'you must be logged in to add a description'})
    # description = data.get('description', '')
    # if not description:
    #     return jsonify({'Error': 'Missing description'})
    # user = getElems(User, {'email': session.get('username')})[0]
    # user['description'] = description
    # createElem(User, user, ['description'])
    # return jsonify({'Success': 'Description added successfully'})

if __name__ == '__main__':
    connectDatabase()
    createTables(User)
    init_bcrypt(app)
    app.run(debug=True, host='localhost', port=8000)
