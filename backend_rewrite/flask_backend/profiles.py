from flask import Blueprint
from flask_jwt_extended import jwt_required
from .decorators import registration_completed

bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')

@bp.route('/me', methods=['GET', 'POST'])
@jwt_required()
@registration_completed
def me():
    """
    Get the current user's profile or update it.
    """
    from flask_jwt_extended import get_jwt_identity, get_jwt
    from .profiles_utils import convert_to_public_profile
    from .db import get_db
    from flask import request, jsonify
    from .user import check_registration_status
    from werkzeug.security import generate_password_hash
    current_user = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (current_user,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'success': False, 'message': 'User not found'})
    if request.method == 'GET':
        profile = convert_to_public_profile(user)
        profile['email'] = user['email']
        return jsonify({'success': True, 'user': profile})
    elif request.method == 'POST':
        try:
            data = request.json
        except:
            return jsonify({'success': False, 'message': 'Invalid JSON'})
        user_informations = {}
        from .user import FIELDS_UPDATABLE, STEP1_FIELDS, STEP2_FIELDS, STEP3_FIELDS, check_fields_step1, check_fields_step2, check_fields_step3, update_user_fields
        for field in FIELDS_UPDATABLE:
            if field in data:
                if type(data[field]) not in [bool, int, str, list]:
                    return jsonify({'success': False, 'message': f'Invalid type for field {field}'})
                if type(data[field]) != int and type(data[field]) != bool:
                    if len(data[field]) == 0:
                        continue
                user_informations[field] = data.get(field, None)
        check = check_registration_status(user["email"])
        if check is False:
            return jsonify({'success': False, 'message': 'User did not complete the registration'})
        else:
            if len(user_informations) == 0:
                return jsonify({'success': False, 'message': 'No field to update'})
            try:
                check_change_mail = False
                check_change_username = False
                if 'email' in user_informations:
                    if user_informations['email'] != user['email']:
                        check_change_mail = True
                elif 'username' in user_informations:
                    if user_informations['username'] != user['username']:
                        check_change_username = True
                result, error  = check_fields_validity(user_informations)
                if result == False:
                    return error
                if 'password' in user_informations:
                    user_informations['password'] = generate_password_hash(user_informations['password'])
                update_user_fields(user_informations, user['email'])
                from .auth import invalidate_token
                if check_change_mail == True or 'password' in user_informations:
                    jti = get_jwt()["jti"]
                    invalidate_token(jti)
                    if check_change_mail == True:
                        from .user import send_confirmation_email
                        if send_confirmation_email(user['email']) == False:
                            print("MAIL ERROR : Failed to send confirmation email")
                    return jsonify({'success': True, 'disconnect': True, 'message': 'User updated successfully, please check your email'})
                return jsonify({'success': True, 'message': 'User updated successfully'})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})

def check_fields_validity(user_informations):
    """
    Check if the fields are valid.
    """
    from flask import jsonify
    from .user import STEP1_FIELDS, STEP2_FIELDS, STEP3_FIELDS, check_fields_step1, check_fields_step2, check_fields_step3
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
    if len(fields["step1"]) > 0:
        result = check_fields_step1(user_informations, fields["step1"], False)
        if result["success"] == False:
            return False, jsonify({'success': False, 'message': ", ".join(result["errors"])})
    if len(fields["step2"]) > 0:
        result = check_fields_step2(user_informations, fields["step2"])
        if result["success"] == False:
            return False, jsonify({'success': False, 'message': ", ".join(result["errors"])})
    if len(fields["step3"]) > 0:
        result = check_fields_step3(user_informations, fields["step3"])
        if result["success"] == False:
            return False, jsonify({'success': False, 'message': ", ".join(result["errors"])})
    return True, None
            
    


@bp.route('/me/views', methods=['GET'])
@jwt_required()
@registration_completed
def get_views():
    """
    Get the current user's views.
    """
    from flask_jwt_extended import get_jwt_identity
    from .profiles_utils import convert_to_public_profile
    from .db import get_db
    from flask import jsonify, current_app
    current_user = get_jwt_identity()
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (current_user,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'message': 'User not found'})
        cur.execute("SELECT * FROM user_views WHERE viewed_id = %s", (user['id'],))
        views = cur.fetchall()
        ids = []
        for view in views:
            ids.append(view['viewer_id'])
        if len(ids) == 0:
            return jsonify({'success': True, 'views': []})
        query = f"""
        {current_app.config['QUERIES'].get('-- get users')}
        WHERE u.id IN %(ids)s
        {current_app.config['QUERIES'].get('-- group by users')}
        """
        cur.execute(query, {'city_id': user['city_id'], 'user_id': user['id'], 'ids': tuple(ids)})
        users = cur.fetchall()
        users = [convert_to_public_profile(u, user) for u in users]
        return jsonify({'success': True, 'views': users})

@bp.route('/me/premium', methods=['POST'])
@jwt_required()
@registration_completed
def premium():
    """
    Upgrade the current user to premium.
    """
    from flask_jwt_extended import get_jwt_identity
    from .db import get_db
    from flask import jsonify
    current_user = get_jwt_identity()
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (current_user,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'message': 'User not found'})
        if user['premium'] == True:
            return jsonify({'success': False, 'message': 'User already premium'})
        cur.execute("UPDATE users SET premium = TRUE WHERE email = %s", (current_user,))
        db.commit()
        return jsonify({'success': True, 'message': 'User upgraded to premium'})

@bp.route('/<int:id>', methods=['GET', 'POST'])
@jwt_required()
@registration_completed
def get_profile(id):
    from .profiles_utils import parse_profile_type
    from .profiles_post_utils import parse_post_actions
    from .user import check_registration_status
    from .db import get_db
    from flask_jwt_extended import get_jwt_identity
    from flask import jsonify, current_app, request
    db = get_db()
    with db.cursor() as cursor:
        user_getting = get_jwt_identity()
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_getting,))
        user_getting = cursor.fetchone()
        if user_getting is None:
            return jsonify({'success': False, 'message': 'User not authenticated'})
        query = f"""
            {current_app.config['QUERIES'].get('-- get users')}
            WHERE u.id = %(id)s
            {current_app.config['QUERIES'].get('-- group by users')}
        """
        cursor.execute(query, {'city_id': user_getting['city_id'], 'user_id': user_getting['id'], 'id': id})
        user = cursor.fetchone()
    if user is None:
        return jsonify({'success': False, 'message': 'User not found'})
    if user['id'] == user_getting['id']:
        return jsonify({'success': False, 'message': 'You cannot get your own profile at this endpoint'})
    if request.method == 'GET':
        result = check_registration_status(user["email"])
        if result is True:
            try:
                return parse_profile_type(user, user_getting)
            except Exception as e:
                print("GET PROFILE : failed to update user views", e)
                return jsonify({'success': False, 'message': 'An error occured'})
        else:
            return jsonify({'success': False, 'message': f'User {user["id"]} did not complete the registration'})
    elif request.method == 'POST':
        try:
            data = request.json
        except:
            print("GET USER FAIL : Json conversion failed :", e)
            return jsonify({'success': False, 'message': 'Invalid JSON'})
        try:
            action = data.get('action', None)
            if action is None:
                return jsonify({'success': False, 'message': 'No action provided'})
            return parse_post_actions(user, user_getting, action)
        except Exception as e:
            print("GET PROFILE FAIL : failed to update user views:", e)
            return jsonify({'success': False, 'message': 'An error occured'})

@bp.route('/profile_pictures', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@registration_completed
def profile_pictures():
    from flask import jsonify, request
    from .profiles_pictures_utils import upload_profile_picture, get_profile_picture, delete_profile_picture
    try:
        if request.method == 'PUT':
            return upload_profile_picture()
        elif request.method == 'GET':
            return get_profile_picture()
        elif request.method == 'DELETE':
            return delete_profile_picture()
        else:
            return jsonify({'success': False, 'message': 'Invalid method'})
    except KeyError as e:
        print("PROFILE PIC FAIL :", e)
        return jsonify({'success': False, 'message': 'An error occured'})
