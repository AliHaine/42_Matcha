from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db
from PIL import Image
import os

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
        return jsonify({'success': False, 'error': 'User not found'})
    return jsonify({'success': True, 'user': convert_to_public_profile(user)}), 200

@bp.route('/<int:id>', methods=['GET', 'POST'])
@jwt_required()
@registration_completed
def get_profile(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    user_getting = get_jwt_identity()
    cursor.execute("SELECT * FROM users WHERE email = %s", (user_getting,))
    user_getting = cursor.fetchone()
    if user is None:
        return jsonify({'success': False, 'error': 'User not found'})
    if user_getting == None:
        return jsonify({'success': False, 'error': 'User not authenticated'})
    if user['id'] == user_getting['id']:
        return jsonify({'success': False, 'error': 'You cannot get your own profile at this endpoint'})
    if request.method == 'GET':
        result = check_registration_status(user["email"])
        if result is True:
            try:
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
                    user_view = cursor.fetchone()
                    if user_view is None:
                        print("updating user views", user_view)
                        cursor.execute("INSERT INTO user_views (viewer_id, viewed_id) VALUES (%s, %s)", (user_getting["id"], user["id"],))
                    else:
                        cursor.execute("UPDATE user_views SET last_view = NOW() WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
                    db.commit()
            except Exception as e:
                print("failed to update user views", e)
            return jsonify({'success': True, 'user': convert_to_public_profile(user)}), 200
        else:
            return jsonify({'success': False, 'error': f'User {user["id"]} did not complete the registration'})
    elif request.method == 'POST':
        try:
            data = request.json
        except:
            return jsonify({'success': False, 'error': 'Invalid JSON'})
        try:
            action = data.get('action', None)
            if action is None:
                return jsonify({'success': False, 'error': 'No action provided'})
            cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
            user_view = cursor.fetchone()
            if user_view is None:
                cursor.execute("INSERT INTO user_views (viewer_id, viewed_id) VALUES (%s, %s)", (user_getting["id"], user["id"],))
                db.commit()
                cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
                user_view = cursor.fetchone()
            if action == 'like':
                cursor.execute("UPDATE user_views SET liked = TRUE WHERE id = %s", (user_view["id"],))
            elif action == 'dislike':
                cursor.execute("UPDATE user_views SET disliked = TRUE WHERE id = %s", (user_view["id"],))
            elif action == 'block':
                cursor.execute("UPDATE user_views SET blocked = TRUE WHERE id = %s", (user_view["id"],))
            elif action == 'unblock':
                cursor.execute("UPDATE user_views SET blocked = FALSE WHERE id = %s", (user_view["id"],))
            elif action == 'report':
                cursor.execute("UPDATE user_views SET reported = TRUE WHERE id = %s", (user_view["id"],))
            else:
                return jsonify({'success': False, 'error': 'Invalid action'})
            db.commit()
            return jsonify({'success': True})
        except Exception as e:
            print("failed to update user views", e)
            return jsonify({'success': False, 'error': 'An error occured'})
    return jsonify({'success': False, 'error': 'Invalid method'})

@bp.route('/profile_pictures', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@registration_completed
def profile_pictures():
    try:
        if request.method == 'PUT':
            print(request.files)
            if 'picture' not in request.files:
                return jsonify({'success': False, 'error': 'No file part'})
            file = request.files['picture']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No selected file'})
            if file and file.filename.split('.')[-1] in current_app.config['PROFILE_PIC_EXTENSIONS']:
                db = get_db()
                current_user = get_jwt_identity()
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (current_user,))
                    user = cursor.fetchone()
                    if user is None:
                        return jsonify({'success': False, 'error': 'User not found'})
                    if user['pictures_number'] >= 5:
                        return jsonify({'success': False, 'error': 'User already has 5 pictures'})
                    filename = f"{user['id']}_{user['pictures_number']}.{file.filename.split('.')[-1]}"
                    file.save(f"{current_app.config['PROFILE_PICTURES_DIR']}/{filename}")
                    if is_image_corrupted(f"{current_app.config['PROFILE_PICTURES_DIR']}/{filename}"):
                        os.remove(f"{current_app.config['PROFILE_PICTURES_DIR']}/{filename}")
                        return jsonify({'success': False, 'error': 'Corrupted image'})
                    cursor.execute("UPDATE users SET pictures_number = pictures_number + 1 WHERE email = %s", (current_user,))
                    db.commit()
                    return jsonify({'success': True}), 200
        elif request.method == 'GET':
            user_id = request.args.get('user_id', None)
            photo_number = request.args.get('photo_number', None)
            if user_id is None:
                return jsonify({'success': False, 'error': 'No user id provided'})
            if photo_number is None:
                return jsonify({'success': False, 'error': 'No photo number provided'})
            try:
                if isinstance(user_id, str):
                    user_id = int(user_id)
                if isinstance(photo_number, str):
                    photo_number = int(photo_number)
                filename = f"{user_id}_{photo_number}"
                file = find_file_without_extension(current_app.config['PROFILE_PICTURES_DIR'], filename)
                if file is None:
                    return jsonify({'success': False, 'error': 'No file found'})
                return send_from_directory(current_app.config['PROFILE_PICTURES_DIR'], f"{filename}.{file.split('.')[-1]}")
            except:
                return jsonify({'success': False, 'error': 'Invalid user id or photo number'})

        elif request.method == 'DELETE':
            file_number = request.args.get('file_number')
            if isinstance(file_number, str):
                try:
                    file_number = int(file_number)
                except:
                    return jsonify({'success': False, 'error': 'Invalid file number'})
            if file_number is None:
                return jsonify({'success': False, 'error': 'No file number provided'})
            if file_number < 0 or file_number > 4:
                return jsonify({'success': False, 'error': 'Invalid file number'})
            db = get_db()
            current_user = get_jwt_identity()
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (current_user,))
                user = cursor.fetchone()
                if user is None:
                    return jsonify({'success': False, 'error': 'User not found'})
                if file_number >= user['pictures_number']:
                    return jsonify({'success': False, 'error': 'No picture at this index'})
                filename = f"{user['id']}_{file_number}"
                file = find_file_without_extension(current_app.config['PROFILE_PICTURES_DIR'], filename)
                os.remove(file)
                cursor.execute("UPDATE users SET pictures_number = pictures_number - 1 WHERE email = %s", (current_user,))
                db.commit()
                realign_photos(user['id'], file_number)
                return jsonify({'success': True}), 200
            return jsonify({'success': False, 'error': 'An error occured'})
        else:
            return jsonify({'success': False, 'error': 'Invalid method'})
    except Exception as e:
        print("exception in profile-picture endpoit", e)
        return jsonify({'success': False, 'error': 'An error occured'})
        
def find_file_without_extension(directory, filename):
    for file in os.listdir(directory):
        if file.startswith(filename + "."):  # Vérifie si le fichier commence par le bon nom
            return os.path.join(directory, file)
    return None

def realign_photos(user_id, file_number):
    for i in range(file_number, 4):
        old_file = find_file_without_extension(current_app.config['PROFILE_PICTURES_DIR'], f"{user_id}_{i+1}")
        if old_file is None:
            break
        new_file = os.path.join(current_app.config['PROFILE_PICTURES_DIR'], f"{user_id}_{i}.{old_file.split('.')[-1]}")
        os.rename(old_file, new_file)

def is_image_corrupted(image):
    try:
        img = Image.open(image)
        img.verify()
        return False
    except Exception as e:
        print(e)
        return True