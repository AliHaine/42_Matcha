import functools
import os
import json

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .db import get_db
from .profiles import convert_to_public_profile

from .decorators import registration_completed

bp = Blueprint('matcha', __name__, url_prefix='/api/matcha')

@bp.route('', methods=['GET'])
@jwt_required()
@registration_completed
def matcha():
    # try:
    #     data = request.json
    # except Exception as e:
    #     return jsonify({'success': False, 'error': 'Invalid parameters'})
    # if data is None:
    #     return jsonify({'success': False, 'error': 'Invalid parameters'})
    # if 'nb_profiles' not in data:
    #     return jsonify({'success': False, 'error': 'Missing parameters'})
    db = get_db()
    nb_profiles = request.args.get('nb_profiles', 1)
    if isinstance(nb_profiles, str):
        try:
            nb_profiles = int(nb_profiles)
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid parameters'})
    user = None
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (get_jwt_identity(),))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'error': 'User not found'})
    if user is None:
        return jsonify({'success': False, 'error': 'User not found'})
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id != %s AND registration_complete = TRUE ORDER BY id ASC', (user["id"],))
        users = cur.fetchall()
        users = [convert_to_public_profile(u) for u in users]
    users_send = []
    for i in range(0, nb_profiles):
        if len(users) == 0:
            break
        rand = os.urandom(1)[0]
        if rand >= len(users) and rand > 0 and len(users) > 0:
            rand = rand % len(users)
        users_send.append(users[rand])
        users.pop(rand)
    return jsonify({'success': True, 'result': users_send}), 200
