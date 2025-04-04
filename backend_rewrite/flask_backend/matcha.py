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
        users_send = [convert_to_public_profile(user) for user in users_send]
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
        "gender": user['gender'],
        "distance": 100,
    }
    cur.execute(base_request, params)
    users = cur.fetchall()
    if users is None or len(users) == 0:
        for _ in range(5):
            params['distance'] += 100
            cur.execute(base_request, params)
            users = cur.fetchall()
            if users is not None and len(users) > 0:
                break
    return users
        
    return users

def second_layer_algo(user=None, user_to_sort=[], nb_profiles=8) -> list | None:
    scored_user_list = []
    for user_target in user_to_sort:
        score = 0.2
        print(user_target)
        user_target['score'] = calcul_score(user, user_target)
        scored_user_list.append(user_target)
    return scored_user_list


def calcul_score(user, user_target):
    score = 0.2
    score += 0.1 if user['smoking'] == user_target['smoking'] else -0.2
    score += 0.1 if user['searching'] == user_target['searching'] else -0.05
    score += 0.1 if user['commitment'] == user_target['commitment'] else -0.05
    score += 0.1 if user['frequency'] == user_target['frequency'] else -0.05

    #The user can have max 1.2 scores from interests, and also earn 0.3 BONUS if there is at least 3 interests in common
    #That mean if the user have 2 interests, score will increase by 0.3, if he have 3 or more, the score will increase by 1.2
    interest_score = 0.0
    if user_target['common_interests'] > 0:
        interest_score = user_target['common_interests'] * 0.3
    if interest_score > 1.2 or interest_score == 0.9:
        interest_score = 1.2
    score += interest_score

    if user['shape'] == user_target['shape']: score += 0.02
    if user['size'] == user_target['size']: score += 0.02
    if user['weight'] == user_target['weight']: score += 0.02

    if score < 0:
        score = 0
    return score

    def convert_score_to_100(score_to_convert):
        pass
