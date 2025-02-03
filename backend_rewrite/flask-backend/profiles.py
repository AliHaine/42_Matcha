from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db

from .decorators import registration_completed

from .user import check_registration_status

bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')


def convert_to_public_profile(user):
    cityID = user['city_id']
    city = ""
    db = get_db()
    if cityID is not None:
        with db.cursor() as cursor:
            cursor.execute("SELECT cityname FROM cities WHERE id = %s", (cityID,))
            cityElement = cursor.fetchone()
            city = cityElement['cityname']
    lookingFor = []
    lookingFor.append(user['searching'])
    lookingFor.append(user['commitment'])
    lookingFor.append(user['frequency'])
    shape = []
    shape.append(user['weight'])
    shape.append(user['size'])
    shape.append(user['shape'])
    health = []
    health.append(user['smoking'])
    health.append(user['alcohol'])
    health.append(user['diet'])
    interests = []
    with db.cursor() as cursor:
        cursor.execute("SELECT interest_id FROM users_interests WHERE user_id = %s", (user['id'],))
        interestsList = cursor.fetchall()
        for interest in interestsList:
            cursor.execute("SELECT name FROM interests WHERE id = %s", (interest['interest_id'],))
            interestElement = cursor.fetchone()
            interests.append(interestElement['name'])
    return {
        'id': user['id'],
        'firstname': user['firstname'],
        'lastname': user['lastname'],
        'age': user['age'],
        'city': city,
        'gender': user['gender'],
        'description': user['description'],
        'lookingFor': lookingFor,
        'shape': shape,
        'health': health,
        'interests': interests,
        'picturesNumber': user['pictures_number'],
        'status': user['status'],
    }

@bp.route('/me', methods=['GET'])
@jwt_required()
@registration_completed
def me():
    current_user = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (current_user,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    return jsonify({'success': True, 'user': convert_to_public_profile(user)}), 200

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@registration_completed
def get_profile(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    result = check_registration_status(user["email"])
    if result is True:
        return jsonify({'success': True, 'user': convert_to_public_profile(user)}), 200
    else:
        return jsonify({'success': False, 'error': f'User {user["id"]} did not complete the registration'}), 400