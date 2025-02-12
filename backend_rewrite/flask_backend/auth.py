import functools
import os
import json

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from .db import get_db

from .user import create_user, check_fields_step1, check_fields_step2, check_fields_step3, update_user_fields, check_registration_status

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

from .decorators import registration_completed

BLACKLIST_FILE = current_app.config["BASE_DIR"] + '/settings/blacklist.json'

def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as file:
            data = json.load(file)
            return set(data)
    return set()

def save_blacklist():
    try:
        os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    except Exception as e:
        print("Failed to create blacklist directory :", e)
    with open(BLACKLIST_FILE, 'w') as file:
        json.dump(list(BLACKLIST), file)

BLACKLIST = load_blacklist()

def register_step1(data):
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
        return jsonify({'success': False, 'error': ", ".join(check['errors'])})
    dup_password = user_informations['password']
    user_informations['password'] = generate_password_hash(user_informations['password'])
    if create_user(user_informations):
        response = login_user(user_informations['email'], dup_password, registering=True)
        print(response)
        if response is None or response['success'] == False:
            return jsonify({'success': False, 'error': 'Failed to login'})
        else:
            return jsonify({'success': True, 'access_token': response['access_token']})
    else:
        return jsonify({'success': False, 'error': 'Failed to create user'})

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
        return jsonify({'success': False, 'error': ", ".join(check['errors'])})
    user_email = get_jwt_identity()
    del user_informations['city']
    result = update_user_fields(user_informations, user_email)
    check_registration_status()
    if result == True:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to update user fields'})

@jwt_required()
def register_step3(data):
    interests = data.get('Culture', [])
    if 'Sport' in data:
        interests.extend(data.get('Sport', []))
    if 'Other' in data:
        interests.extend(data.get('Other', []))
    user_informations = {
        'interests': interests,
        'description': data.get('description', ''),
    }
    check = check_fields_step3(user_informations)
    if check['success'] == False:
        return jsonify({'success': False, 'error': ", ".join(check['errors'])})
    user_email = get_jwt_identity()
    result = update_user_fields(user_informations, user_email)
    check_registration_status()
    if result == True:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to update user fields'})
    

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
    except Exception as e:
        print("crash at json conversion :", e)
        return jsonify({'success': False, 'error': 'Invalid JSON'})
    step = data.get("step", 0)
    if step == 2 or step == 3:
        result = check_registration_status()
        if result == True:
            return jsonify({'success': False, 'error': 'User already completed the registration'})
    if step == 1:
        return register_step1(data)
    elif step == 2:
        return register_step2(data)
    elif step == 3:
        return register_step3(data)
    else:
        return jsonify({'success': False, 'error': 'Invalid step'})
    
    

def login_user(email, password, registering=False):
    check = check_fields_step1({'email': email, 'password': password}, ['email', 'password'], email_exists_check=False)
    if check['success'] == False:
        return {'success': False, 'error': "".join(check['errors'])}
    db = get_db()
    missing_steps = []
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        if user is None:
            return {'success': False, 'error':'User not found'}
        step1_fields = ['email', 'password', 'firstname', 'lastname', 'age', 'gender']
        for field in step1_fields:
            if user[field] is None:
                missing_steps.append(1)
                break
        step2_fields = ['searching', 'commitment', 'frequency', 'weight', 'size', 'shape', 'smoking', 'alcohol', 'diet']
        for field in step2_fields:
            if user[field] is None:
                missing_steps.append(2)
                break
        step3_fields = ['description']
        for field in step3_fields:
            if user[field] is None:
                missing_steps.append(3)
                break
        
    if user is None or not check_password_hash(user['password'], password):
        return {'success': False, 'error': 'Invalid email or password'}
    access_token = create_access_token(identity=user['email'])
    if registering == False:
        if len(missing_steps) > 0:
            return {'success': False, 'error': 'Registration not completed', 'missing_steps': missing_steps, 'access_token': access_token}
    return {'success': True, 'access_token': access_token}

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    response = login_user(email, password)
    if response is None or response['success'] == False:
        if 'missing_steps' in response:
            return jsonify({'success': False, 'error': 'Registration not completed', 'missing_steps': response['missing_steps'], 'access_token': response['access_token']})
        return jsonify({'success': False, 'error': 'Failed to login'})
    else:
        return jsonify({'success': True, 'access_token': response['access_token']})

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Récupère l'ID unique du token
    BLACKLIST.add(jti)  # Ajoute à la liste noire
    save_blacklist()
    return jsonify({"msg": "Successfully logged out"})


@bp.route('/verify_token', methods=['GET'])
@jwt_required()
@registration_completed
def verify_token():
    user_email = get_jwt_identity()
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (user_email,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'error': 'User not found'})
    return jsonify({'success': True}), 200