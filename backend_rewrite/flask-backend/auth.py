import functools
import os
import json

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from .db import get_db

from .user import create_user, check_fields_step1, check_fields_step2, check_fields_step3, update_user_fields, check_registration_status

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


BLACKLIST_FILE = current_app.config["BASE_DIR"] + '/settings/blacklist.json'

def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as file:
            data = json.load(file)
            return set(data)
    return set()

def save_blacklist():
    with open(BLACKLIST_FILE, 'w') as file:
        json.dump(list(BLACKLIST), file)

BLACKLIST = load_blacklist()

def register_step1(data):
    if verify_jwt_in_request(optional=True):
        print("verify_jwt_in_request")
        jti = get_jwt()["jti"]  # Récupère l'ID unique du token
        BLACKLIST.add(jti)
        save_blacklist()
    user_informations = {
        'firstname': data.get('firstname', ''),
        'lastname': data.get('lastname', ''),
        'email': data.get('email', ''),
        'password': data.get('password', ''),
        'age': data.get('age', 0),
        'gender': data.get('gender', ''),
    }
    check = check_fields_step1(user_informations)
    if check['success'] == False:
        return jsonify({'success': False, 'error': ", ".join(check['errors'])}), 400
    dup_password = user_informations['password']
    user_informations['password'] = generate_password_hash(user_informations['password'])
    if create_user(user_informations):
        response = login_user(user_informations['email'], dup_password)
        print(response)
        if response is None or response['success'] == False:
            return jsonify({'success': False, 'error': 'Failed to login'}), 400
        else:
            return jsonify({'success': True, 'access_token': response['access_token']}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to create user'}), 400

@jwt_required()
def register_step2(data):
    user_informations = {
        'city': data.get('city', {}),
        'searching': data.get('searching', ''),
        'commitment': data.get('commitment', ''),
        'frequency': data.get('frequency', ''),
        'weight': data.get('weight', ''),
        'size': data.get('size', ''),
        'shape': data.get('shape', ''),
        'smoking': data.get('smoking', None),
        'alcohol': data.get('alcohol', ''),
        'diet': data.get('diet', ''),
    }
    check = check_fields_step2(user_informations)
    if check['success'] == False:
        return jsonify({'success': False, 'error': ", ".join(check['errors'])}), 400
    user_email = get_jwt_identity()
    result = update_user_fields(user_informations, user_email)
    check_registration_status()
    if result == True:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update user fields'}), 400

@jwt_required()
def register_step3(data):
    interests = data.get('artCulture', [])
    interests += data.get('sportActivity', [])
    interests += data.get('other', [])
    user_informations = {
        'interests': interests,
        'description': data.get('description', ''),
    }
    check = check_fields_step3(user_informations)
    if check['success'] == False:
        return jsonify({'success': False, 'error': ", ".join(check['errors'])}), 400
    user_email = get_jwt_identity()
    result = update_user_fields(user_informations, user_email)
    check_registration_status()
    if result == True:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update user fields'}), 400
    

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
    except Exception as e:
        print("crash at json conversion :", e)
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    step = data.get("step", 0)
    if step == 2 or step == 3:
        result = check_registration_status()
        if result == True:
            return jsonify({'success': False, 'error': 'User already completed the registration'}), 400
    if step == 1:
        return register_step1(data)
    elif step == 2:
        return register_step2(data)
    elif step == 3:
        return register_step3(data)
    else:
        return jsonify({'success': False, 'error': 'Invalid step'}), 400
    
    

def login_user(email, password):
    check = check_fields_step1({'email': email, 'password': password}, ['email', 'password'], email_exists_check=False)
    if check['success'] == False:
        return {'success': False, 'error': "".join(check['errors'])}
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
    if user is None or not check_password_hash(user['password'], password):
        return {'success': False, 'error': 'Invalid email or password'}
    access_token = create_access_token(identity=user['email'])
    return {'success': True, 'access_token': access_token}

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    response = login_user(email, password)
    if response is None or response['success'] == False:
        return jsonify({'success': False, 'error': 'Failed to login'}), 400
    else:
        return jsonify({'success': True, 'access_token': response['access_token']})

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Récupère l'ID unique du token
    BLACKLIST.add(jti)  # Ajoute à la liste noire
    save_blacklist()
    return jsonify({"msg": "Successfully logged out"}), 200
