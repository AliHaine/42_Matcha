import functools

from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .db import get_db

from .user import create_user, check_fields_step1, check_fields_step2, update_user_fields

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

BLACKLIST = set()

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
        return jsonify({'success': False, 'error': "".join(check['errors'])}), 400
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
        return jsonify({'success': False, 'error': "".join(check['errors'])}), 400
    user_email = get_jwt_identity()
    del user_informations['city']
    result = update_user_fields(user_informations, user_email)
    if result == True:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update user fields'}), 400
    



@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    step = data.get("step", 0)
    if step == 1:
        return register_step1(data)
    elif step == 2:
        return register_step2(data)
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
    return jsonify({"msg": "Successfully logged out"}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    email = get_jwt_identity()
    return jsonify({'success': True, 'user_email': email}), 200
