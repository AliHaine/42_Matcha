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
            return jsonify({'success': False, 'error': 'User not found'}), 404

        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (user_mail,))
            user = cur.fetchone()
            if user is None:
                return jsonify({'success': False, 'error': 'User not found'}), 404

            if user['registration_complete'] == True:
                return f(*args, **kwargs)
            else:
                step1_fields = ['email', 'password', 'firstname', 'lastname', 'age', 'gender']
                step2_fields = ['searching', 'commitment', 'frequency', 'weight', 'size', 'shape', 'smoking', 'alcohol', 'diet']
                step3_fields = ['description']
                for field in step1_fields:
                    if user[field] is None:
                        return jsonify({'success': False, 'error': 'Registration not completed', 'step':1}), 400
                for field in step2_fields:
                    if user[field] is None:
                        return jsonify({'success': False, 'error': 'Registration not completed', 'step':2}), 400
                for field in step3_fields:
                    if user[field] is None:
                        return jsonify({'success': False, 'error': 'Registration not completed', 'step':3}), 400
                cur.execute('SELECT * FROM users_interests WHERE user_id = %s', (user['id'],))
                interests = cur.fetchall()
                if len(interests) == 0:
                    return jsonify({'success': False, 'error': 'Registration not completed', 'step':3}), 400
                cur.execute('UPDATE users SET registration_complete = TRUE WHERE email = %s', (user_mail,))
        return f(*args, **kwargs)

    return decorated_function
