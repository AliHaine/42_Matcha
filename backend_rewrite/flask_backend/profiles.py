from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .db import get_db
from PIL import Image
import os

from werkzeug.security import generate_password_hash

from .decorators import registration_completed

from .user import check_registration_status

bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')

def convert_to_public_profile(user, user_requesting=None):
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
    matching = "none"
    with db.cursor() as cursor:
        cursor.execute("SELECT interest_id FROM users_interests WHERE user_id = %s", (user['id'],))
        interestsList = cursor.fetchall()
        for interest in interestsList:
            cursor.execute("SELECT name FROM interests WHERE id = %s", (interest['interest_id'],))
            interestElement = cursor.fetchone()
            interests.append(interestElement['name'])
        if user_requesting is not None:
            cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (user_requesting['id'], user['id'],))
            user_view = cursor.fetchone()
            if user_view is not None:
                if user_view["blocked"] == True:
                    matching = "block"
                elif user_view["liked"] == True:
                    matching = "like"
                    cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s AND liked = TRUE", (user['id'], user_requesting['id'],))
                    user_viewed = cursor.fetchone()
                    if user_viewed is not None:
                        if user_viewed["liked"] == True:
                            matching = "match"
        else:
            matching = "none"
    return {
        'id': user['id'],
        'firstname': user['firstname'],
        'lastname': user['lastname'],
        'age': user['age'],
        'city': city,
        'gender': user['gender'],
        'description': user['description'],
        'hetero': user['hetero'],
        'lookingFor': lookingFor,
        'shape': shape,
        'health': health,
        'interests': interests,
        'picturesNumber': user['pictures_number'],
        'status': user['status'],
        'fame_rate': user['fame_rate'],
        "matching": matching,
        "email_verified": user['email_verified']
    }

def convert_to_chat_profile(user, user_getting, all_messages=False):
    cityID = user['city_id']
    city = ""
    db = get_db()
    if cityID is not None:
        with db.cursor() as cursor:
            cursor.execute("SELECT cityname FROM cities WHERE id = %s", (cityID,))
            cityElement = cursor.fetchone()
            city = cityElement['cityname']
    base_return = {
        'id': user['id'],
        'firstname': user['firstname'],
        'age': user['age'],
        'city': city,
        'picturesNumber': user['pictures_number'],
        'status': user['status'],
    }
    with db.cursor() as cursor:
        if all_messages == True:
            cursor.execute("SELECT * FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY created_at ASC", (user['id'], user_getting['id'], user_getting['id'], user['id'],))
            allMessages = cursor.fetchall()
            if allMessages:
                messages = []
                for message in allMessages:
                    messages.append({
                        'message': message['message'],
                        'created_at': message['created_at'].strftime("%H:%M"),
                        'author_id': message['sender_id'],
                    })
                base_return.update({
                    'allMessages': messages,
                })
        else:
            cursor.execute("SELECT * FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY created_at DESC LIMIT 1", (user['id'], user_getting['id'], user_getting['id'], user['id'],))
            lastMessage = cursor.fetchall()
            if lastMessage:
                message = {
                    'message': lastMessage[0]['message'],
                    'created_at': lastMessage[0]['created_at'].strftime("%H:%M"),
                    'author_id': lastMessage[0]['sender_id'],
                }
                base_return.update({
                    'lastMessage': message,
                })
        return base_return
    


@bp.route('/me', methods=['GET', 'POST'])
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
    if request.method == 'GET':
        profile = convert_to_public_profile(user)
        profile['email'] = user['email']
        return jsonify({'success': True, 'user': profile})
    elif request.method == 'POST':
        try:
            data = request.json
        except:
            return jsonify({'success': False, 'error': 'Invalid JSON'})
        user_informations = {}
        from .user import FIELDS_UPDATABLE, STEP1_FIELDS, STEP2_FIELDS, STEP3_FIELDS, check_fields_step1, check_fields_step2, check_fields_step3, update_user_fields
        for field in FIELDS_UPDATABLE:
            if field in data:
                if type(data[field]) != int and type(data[field]) != bool:
                    if len(data[field]) == 0:
                        continue
                user_informations[field] = data.get(field, None)
        check = check_registration_status(user["email"])
        if check is False:
            return jsonify({'success': False, 'error': 'User did not complete the registration'})
        else:
            if len(user_informations) == 0:
                return jsonify({'success': False, 'error': 'No field to update'})
            try:
                check_change_mail = False
                if 'email' in user_informations:
                    if user_informations['email'] != user['email']:
                        check_change_mail = True
                fields = {
                    "step1": [],
                    "step2": [],
                    "step3": []
                }
                for field in user_informations:
                    if field in STEP1_FIELDS:
                        fields["step1"].append(field)
                    elif field in STEP2_FIELDS:
                        fields["step2"].append(field)
                    elif field in STEP3_FIELDS:
                        fields["step3"].append(field)
                print("fields : ", fields, end="\n\n\n\n")
                if len(fields["step1"]) > 0:
                    result = check_fields_step1(user_informations, email_exists_check=check_change_mail, fields=fields["step1"])
                    if result["success"] is False:
                        return jsonify({'success': False, 'error': ", ".join(result['errors'])})
                if len(fields["step2"]) > 0:
                    result = check_fields_step2(user_informations, fields=fields["step2"])
                    if result["success"] is False:
                        return jsonify({'success': False, 'error': ", ".join(result['errors'])})
                if len(fields["step3"]) > 0:
                    result = check_fields_step3(user_informations, fields=fields["step3"])
                    if result["success"] is False:
                        return jsonify({'success': False, 'error': ", ".join(result['errors'])})
                if 'password' in user_informations:
                    print("changing password : ", user_informations['password'], end="\n\n\n\n")
                    user_informations['password'] = generate_password_hash(user_informations['password'])
                print("user informations : ", user_informations, end="\n\n\n\n")
                update_user_fields(user_informations, user['email'])
                db.commit()
                from .auth import invalidate_token
                if check_change_mail == True or 'password' in user_informations:
                    invalidate_token(user['email'])
                    return jsonify({'success': True, 'disconnect': True})
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})

@bp.route('/me/views', methods=['GET'])
@jwt_required()
@registration_completed
def get_views():
    current_user = get_jwt_identity()
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (current_user,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'error': 'User not found'})
        cur.execute("SELECT * FROM user_views WHERE viewed_id = %s", (user['id'],))
        views = cur.fetchall()
        ids = []
        for view in views:
            ids.append(view['viewer_id'])
        cur.execute("SELECT * FROM users WHERE id IN %s", (tuple(ids),))
        users = cur.fetchall()
        users = [convert_to_public_profile(u, user) for u in users]
        return jsonify({'success': True, 'views': users})
        

@bp.route('/<int:id>', methods=['GET', 'POST'])
@jwt_required()
@registration_completed
def get_profile(id):
    from .websocket import send_notification
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
                        cursor.execute("INSERT INTO user_views (viewer_id, viewed_id, accessed) VALUES (%s, %s, TRUE)", (user_getting["id"], user["id"],))
                    else:
                        cursor.execute("UPDATE user_views SET last_view = NOW(), accessed = TRUE WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
                    if 'chat' in request.args and request.args['chat'] != 'true':
                        send_notification(user_getting["id"], user["id"], "view", "User viewed your profile")
                    db.commit()
            except Exception as e:
                print("failed to update user views", e)
            if 'chat' in request.args and request.args['chat'] == 'true':
                if 'all_messages' in request.args and request.args['all_messages'] == 'true':
                    return jsonify({'success': True, 'user': convert_to_chat_profile(user, user_getting, all_messages=True), 'chat': True})
                return jsonify({'success': True, 'user': convert_to_chat_profile(user, user_getting), 'chat': True})
            return jsonify({'success': True, 'user': convert_to_public_profile(user, user_getting)})
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
            print("data received : ", data)
            cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
            user_view = cursor.fetchone()
            if user_view is None:
                cursor.execute("INSERT INTO user_views (viewer_id, viewed_id) VALUES (%s, %s)", (user_getting["id"], user["id"],))
                db.commit()
                cursor.execute("SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s", (user_getting["id"], user["id"],))
                user_view = cursor.fetchone()
            print("user view", user_view)
            if action == 'like':
                if user_view["blocked"]:
                    return jsonify({'success': False, 'error': 'User is blocked'})
                liked = False
                if user_view["liked"] == True:
                    cursor.execute("UPDATE user_views SET liked = FALSE WHERE id = %s", (user_view["id"],))
                    send_notification(user_getting["id"], user["id"], "dislike", "User unliked your profile")
                else:
                    cursor.execute("UPDATE user_views SET liked = TRUE WHERE id = %s", (user_view["id"],))
                    send_notification(user_getting["id"], user["id"], "like", "User liked your profile")
                    liked = True
                cursor.execute('SELECT * FROM user_views WHERE viewer_id = %s AND viewed_id = %s AND liked = TRUE', (user["id"], user_getting["id"],))
                user_viewed = cursor.fetchone()
                print("user viewed", user_viewed)
                if user_viewed is not None:
                    print("user viewed", user_viewed)
                    if user_viewed["liked"] == True:
                        if liked == True:
                            send_notification(user["id"], user_getting["id"], "match", "User matched with you")
                            send_notification(user_getting["id"], user["id"], "match", "User matched with you")
                        else:
                            send_notification(user["id"], user_getting["id"], "unmatch", "User unmatched with you")
                            send_notification(user_getting["id"], user["id"], "unmatch", "User unmatched with you")
                db.commit()
            elif action == 'block':
                if user_view["blocked"] == True:
                    cursor.execute("UPDATE user_views SET blocked = FALSE WHERE id = %s", (user_view["id"],))
                    send_notification(user_getting["id"], user["id"], "unblock", "User unblocked you")
                else:
                    cursor.execute("UPDATE user_views SET blocked = TRUE WHERE id = %s", (user_view["id"],))
                    send_notification(user_getting["id"], user["id"], "block", "User blocked you")
            elif action == 'report':
                cursor.execute("UPDATE user_views SET reported = TRUE WHERE id = %s", (user_view["id"],))
            else:
                return jsonify({'success': False, 'error': 'Invalid action'})
            db.commit()
            return jsonify({'success': True})
        except Exception as e:
            print("failed to update user views", e, end="\n\n\n\n")
            return jsonify({'success': False, 'error': 'An error occured'})
    return jsonify({'success': False, 'error': 'Invalid method'})

@bp.route('/profile_pictures', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@registration_completed
def profile_pictures():
    try:
        if request.method == 'PUT':
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