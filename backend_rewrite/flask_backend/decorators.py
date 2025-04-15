from functools import wraps
from flask import jsonify, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from .db import get_db

def registration_completed(f):
    @jwt_required()
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_mail = get_jwt_identity()
        if not user_mail:
            return jsonify({'success': False, 'error': 'User not found'})
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (user_mail,))
            user = cur.fetchone()
            if user is None:
                return jsonify({'success': False, 'error': 'User not found'})
            if user['registration_complete'] == True:
                return f(*args, **kwargs)
            else:
                from .user import STEP1_FIELDS, STEP2_FIELDS, STEP3_FIELDS
                step1_fields = STEP1_FIELDS
                step2_fields = STEP2_FIELDS
                step3_fields = STEP3_FIELDS
                if 'interests' in step3_fields:
                    step3_fields.remove('interests')
                if 'city' in step2_fields:
                    step2_fields.remove('city')
                for field in step1_fields:
                    if user[field] is None:
                        return jsonify({'success': False, 'error': 'Registration not completed', 'step':1})
                for field in step2_fields:
                    if user[field] is None:
                        return jsonify({'success': False, 'error': 'Registration not completed', 'step':2})
                for field in step3_fields:
                    if user[field] is None:
                        return jsonify({'success': False, 'error': 'Registration not completed', 'step':3})
                if user['city_id'] is None:
                    return jsonify({'success': False, 'error': 'Registration not completed', 'step':2})
                cur.execute('SELECT * FROM users_interests WHERE user_id = %s', (user['id'],))
                interests = cur.fetchall()
                if len(interests) == 0:
                    return jsonify({'success': False, 'error': 'Registration not completed', 'step':3})
                cur.execute('UPDATE users SET registration_complete = TRUE WHERE email = %s', (user_mail,))
                db.commit()

        return f(*args, **kwargs)
    return decorated_function
