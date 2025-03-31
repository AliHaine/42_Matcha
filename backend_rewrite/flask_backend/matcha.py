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
    nb_profiles = request.args.get('nb_profiles', 1)
    if isinstance(nb_profiles, str):
        try:
            nb_profiles = int(nb_profiles)
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid parameters'})
    if nb_profiles <= 0:
        return jsonify({'success': False, 'error': 'Invalid parameters'})
    user = None
    users_send = []
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (get_jwt_identity(),))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'error': 'User not found'})
        list_of_users = first_layer_algo(user, cur)
        if list_of_users is None or len(list_of_users) == 0:
            return jsonify({'success': False, 'error': 'No users found'})
        users_send = second_layer_algo(user, list_of_users, nb_profiles)
        if users_send is None or len(users_send) == 0:
            return jsonify({'success': False, 'error': 'No users found'})
    return jsonify({'success': True, 'result': users_send}), 200


def first_layer_algo(user=None, cur=None) -> dict | None:
    # base request get all users where the user is not the same as requesting user, get the distance between the two users, and get the common interests
    db = get_db()
    cur = db.cursor()
    base_request = current_app.config['QUERIES'].get("-- matcha default", None)
    if base_request is None:
        return None
    params = {
        "user_id": user['id'],
        "city_id": user['city_id'],
        "age_min": user['age'] - 3,
        "age_max": user['age'] + 3,
        "hetero": user['hetero'],
        "gender": user['gender']
    }
    print(cur.mogrify(base_request, params))
    cur.execute(base_request, params)
    users = cur.fetchall()
    return users

def second_layer_algo(user=None, user_to_sort=[], nb_profiles=8) -> dict | None:
    pass