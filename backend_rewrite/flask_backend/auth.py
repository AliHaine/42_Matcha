import functools
import os
import json

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
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
        if not os.path.exists(os.path.dirname(BLACKLIST_FILE)):
            os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    except Exception as e:
        print("Failed to create blacklist directory :", e)
    with open(BLACKLIST_FILE, 'w') as file:
        json.dump(list(BLACKLIST), file)

def invalidate_token(jti):
    BLACKLIST.add(jti)
    save_blacklist()

def is_token_revoked(jti):
    return jti in BLACKLIST

BLACKLIST = load_blacklist()

def register_step1(data):
    user_informations = {
        'firstname': data.get('firstname', ''),
        'hetero': data.get('hetero', None),
        'lastname': data.get('lastname', ''),
        'email': data.get('email', ''),
        'password': data.get('password', ''),
        'age': data.get('age', 0),
        'gender': data.get('gender', ''),
        'username': data.get('username', ''),
    }
    check = check_fields_step1(user_informations)
    if check['success'] == False:
        return jsonify({'success': False, 'message': ", ".join(check['errors'])})
    dup_password = user_informations['password']
    user_informations['password'] = generate_password_hash(user_informations['password'])
    if create_user(user_informations):
        from .user import send_confirmation_email
        if send_confirmation_email(user_informations['email']) == False:
            return jsonify({'success': False, 'message': 'Failed to send confirmation email'})
        return jsonify({'success': True, 'message': 'User created successfully, please check your email to confirm your account before logging in to continue your registration'})
    else:
        return jsonify({'success': False, 'message': 'Failed to create user'})

@jwt_required()
def register_step2(data):
    user_informations = {
        'city': data.get('city', ""),
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
        return jsonify({'success': False, 'message': ", ".join(check['errors'])})
    user_email = get_jwt_identity()
    result = update_user_fields(user_informations, user_email)
    check_registration_status()
    if result == True:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to update user fields'})

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
        return jsonify({'success': False, 'message': ", ".join(check['errors'])})
    user_email = get_jwt_identity()
    result = update_user_fields(user_informations, user_email)
    check_registration_status()
    if result == True:
        return jsonify({'success': True, 'message': 'Registration completed'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update user fields'})
    
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
    except Exception as e:
        print("REGISTER ERROR : Failed to get json :", e)
        return jsonify({'success': False, 'message': 'Invalid JSON'})
    step = data.get("step", 0)
    if step == 2 or step == 3:
        result = check_registration_status()
        if result == True:
            return jsonify({'success': False, 'message': 'User already completed the registration'})
    if step == 1:
        return register_step1(data)
    elif step == 2:
        return register_step2(data)
    elif step == 3:
        return register_step3(data)
    else:
        return jsonify({'success': False, 'message': 'Invalid step'})
    
    

def login_user(username, password, registering=False):
    missing_steps = []
    db = get_db()
    if type(username) != str or type(password) != str:
        return {'success': False, 'error': 'Invalid username or password'}
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        if user is None:
            return {'success': False, 'error':'Invalid username'}
        if not check_password_hash(user['password'], password):
            return {'success': False, 'error': 'Invalid password'}
        if user['email_verified'] == False:
            return {'success': False, 'error': 'Email not verified'}
        if user["registration_complete"] == False:
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
    access_token = create_access_token(identity=user['email'])
    if registering == False:
        if len(missing_steps) > 0:
            return {'success': False, 'error': 'Registration not completed', 'missing_steps': missing_steps, 'access_token': access_token}
    return {'success': True, 'access_token': access_token}

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
    except Exception as e:
        print("LOGIN ERROR : Failed to get json :", e)
        return jsonify({'success': False, 'message': 'Invalid JSON'})
    username = data.get('username', '')
    password = data.get('password', '')
    response = login_user(username, password)
    if response is None or response['success'] == False:
        if 'missing_steps' in response:
            return jsonify({'success': False, 'message': 'Registration not completed', 'missing_steps': response['missing_steps'], 'access_token': response['access_token']})
        if 'error' in response:
            return jsonify({'success': False, 'message': response['error']})
        return jsonify({'success': False, 'message': 'Failed to login'})
    else:
        return jsonify({'success': True, 'access_token': response['access_token']})

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    invalidate_token(get_jwt()['jti'])
    return jsonify({'success': True, "message": "Successfully logged out"})


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
            return jsonify({'success': False, 'message': 'User not found'})
    return jsonify({'success': True})

@bp.route('/confirm_email', methods=['POST'])
def confirm_email():
    db = get_db()
    try:
        data = request.json
    except Exception as e:
        print("CONFIRM EMAIL ERROR : Failed to get json :", e)
        return jsonify({'success': False, 'message': 'Invalid JSON'})
    token = data.get('token', None)
    if token is None:
        return jsonify({'success': False, 'message': 'No token provided'})
    if type(token) != str:
        return jsonify({'success': False, 'message': 'Invalid token'})
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email_token = %s', (token,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'message': 'User not found'})
        if user['email_verified'] == True:
            return jsonify({'success': True, 'message': 'Email already verified'})
        if user['email_token'] != token:
            return jsonify({'success': False, 'message': 'Invalid token'})
        cur.execute('UPDATE users SET email_verified = TRUE, email_token = NULL WHERE email = %s', (user['email'],))
        db.commit()
    return jsonify({'success': True, 'message': 'Email verified successfully'})

@bp.route('/get_reset_password', methods=['POST'])
def get_reset_password():
    try:
        data = request.json
    except Exception as e:
        print("GET RESET PASS ERROR : Failed to get json :", e)
        return jsonify({'success': False, 'message': 'Invalid JSON'})
    email = data.get('email', '')
    if type(email) != str:
        return jsonify({'success': False, 'message': 'Invalid email'})
    if email == '':
        return jsonify({'success': False, 'message': 'Email not provided'})
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'message': 'User not found'})
        from .user import send_reset_password_email
        if send_reset_password_email(user['email']) == False:
            return jsonify({'success': False, 'message': 'Failed to send reset password email'})
    return jsonify({'success': True, 'message': 'Reset password email sent successfully'})

@bp.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.json
    except Exception as e:
        print("RESET PASS ERROR : Failed to get json :", e)
        return jsonify({'success': False, 'message': 'Invalid JSON'})
    token = data.get('token', '')
    password = data.get('password', '')
    if type(token) != str:
        return jsonify({'success': False, 'message': 'Invalid token'})
    if type(password) != str:
        return jsonify({'success': False, 'message': 'Invalid password'})
    if token == '' or password == '':
        return jsonify({'success': False, 'message': 'Email, token or password not provided'})
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE reset_token = %s', (token,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'message': 'User not found'})
        import datetime
        if user["expiration"] < datetime.datetime.now():
            return jsonify({'success': False, 'message': 'Token expired'})
        from .user import check_fields_step1
        ret = check_fields_step1({'password': password}, ['password'])
        if ret['success'] == False:
            return jsonify({'success': False, 'message': ", ".join(ret['errors'])})
        hashed_password = generate_password_hash(password)
        cur.execute('UPDATE users SET password = %s, reset_token = NULL, expiration = NULL WHERE id = %s', (hashed_password, user['id']))
        db.commit()
    return jsonify({'success': True, 'message': 'Password reset successfully'})