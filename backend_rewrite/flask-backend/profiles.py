from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db
from PIL import Image

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

@bp.route('/profile_pictures', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@registration_completed
def profile_pictures():
    if request.method == 'PUT':
        print(request.files)
        if 'picture' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'}), 400
        file = request.files['picture']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400
        if file and file.filename.split('.')[-1] in current_app.config['PROFILE_PIC_EXTENSIONS']:
            if is_image_corrupted(file):
                return jsonify({'success': False, 'error': 'Corrupted image'}), 400
            current_user = get_jwt_identity()
            db = get_db()
            try:
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (current_user,))
                    user = cursor.fetchone()
                    if user is None:
                        return jsonify({'success': False, 'error': 'User not found'}), 404
                    if user['pictures_number'] >= 5:
                        return jsonify({'success': False, 'error': 'User already has 5 pictures'}), 400
                    filename = f"{user['id']}_{user['pictures_number']}.{file.filename.split('.')[-1]}"
                    file.save(f"{current_app.config['PROFILE_PICTURES_DIR']}/{filename}")
                    cursor.execute("UPDATE users SET pictures_number = pictures_number + 1 WHERE email = %s", (current_user,))
                    db.commit()
            except Exception as e:
                print(e)
                return jsonify({'success': False, 'error': 'Failed to update user pictures'}), 400
    elif request.method == 'GET':
        return jsonify({'success': False, 'error': 'not implemented yet'}), 200
    elif request.method == 'DELETE':
        return jsonify({'success': False, 'error': 'not implemented yet'}), 200


def is_image_corrupted(image):
    try:
        img = Image.open(image)
        img.verify()
        return False
    except Exception as e:
        print(e)
        return True