from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from database import connectDatabase, createTables, createElem, getElems
from models.user import User, create_user, ALLOED_CHARACTERS, PASSWORD_REQUIREMENTS, login_user_func
from crypting import init_bcrypt

app = Flask(__name__)


CORS(app)

@app.route('/api/register', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/register', methods=['POST'])
def register_user():
    values = request.json
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
        return jsonify({'Success': 'User created successfully'})
    except Exception as e:
        return jsonify({'Error': str(e)})

@app.route('/api/login', methods=['POST'])
def loginRoute():
    data = request.json
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

@app.route('/api/registerRequirements', methods=['GET'])
def get_register_requirements():
    # return ALLOED_CHARACTERS, PASSWORD_REQUIREMENTS
    return jsonify({'banned_charactes': ALLOED_CHARACTERS, 'password_requirements': PASSWORD_REQUIREMENTS, 'required fields': ['firstName', 'lastName', 'email', 'password', 'passwordConfirm']})

if __name__ == '__main__':
    connectDatabase()
    createTables(User)
    init_bcrypt(app)
    app.run(debug=True, host='localhost', port=8000)
