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

            step1_fields = ["firstname", "lastname", "email", "password", "age", "gender"]
            for field in step1_fields:
                if field not in user or user[field] is None:
                    return jsonify({'success': False, 'error': "Step 1 is not completed", "step": 1}), 400

            step2_fields = ["city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet"]
            for field in step2_fields:
                if field not in user or user[field] is None:
                    return jsonify({'success': False, 'error': "Step 2 is not completed", "step": 2}), 400
        return f(*args, **kwargs)

    return decorated_function
