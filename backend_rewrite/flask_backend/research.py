from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db
from PIL import Image
import os

from .profiles import convert_to_public_profile

from .decorators import registration_completed

bp = Blueprint('research', __name__, url_prefix='/api/research')

@bp.route('', methods=['GET'])
@jwt_required()
@registration_completed
def research():
    profile_per_page = request.args.get('profile_per_page', None)
    page = request.args.get('page', None)
    research_results = []
    if profile_per_page is None or page is None:
        return jsonify({'error': 'Missing parameters'})
    try:
        if isinstance(profile_per_page, str):
            profile_per_page = int(profile_per_page)
        if isinstance(page, str):
            page = int(page)
    except Exception as e:
        return jsonify({'error': 'Invalid parameters'})
    if profile_per_page < 1 or page < 1:
        return jsonify({'error': 'Invalid parameters'})
    arguments = {}
    errors = []
    try:
        if 'ageMin' in request.args:
            if not request.args['ageMin'].isdigit():
                errors.append('Invalid ageMin')
            else:
                arguments['age_min'] = int(request.args['ageMin'])
        if 'ageMax' in request.args:
            if not request.args['ageMax'].isdigit():
                errors.append('Invalid ageMax')
            else:
                arguments['age_max'] = int(request.args['ageMax'])
        if 'location' in request.args:
            arguments['location'] = request.args['location']
        if 'interest' in request.args:
            arguments['interest'] = request.args['interest']
        if 'fameRate' in request.args:
            fame_rate = request.args['fameRate']
            if fame_rate == 'true':
                arguments['fame_rate'] = True
            elif fame_rate == 'false':
                arguments['fame_rate'] = False
            else:
                errors.append('Invalid fameRate')
        if 'showBlocks' in request.args:
            fame_rate = request.args['showBlocks']
            if fame_rate == 'true':
                arguments['show_blocks'] = True
            elif fame_rate == 'false':
                arguments['show_blocks'] = False
            else:
                errors.append('Invalid fameRate')
    except Exception as e:
        print("failed arguments research", e)
        return jsonify({'error': 'Invalid parameters'})
    db = get_db()
    with db.cursor() as cur:
        baseRequest = 'SELECT * FROM users WHERE email != %s AND registration_complete = TRUE'
        if 'age_min' in arguments:
            baseRequest += f' AND age >= {arguments["age_min"]}'
        if 'age_max' in arguments:
            baseRequest += f' AND age <= {arguments["age_max"]}'
        if 'location' in arguments:
            cur.execute('SELECT id FROM cities WHERE cityname = %s', (arguments['location'],))
            location = cur.fetchone()
            if location is None:
                errors.append('Invalid location')
            else:
                baseRequest += f' AND city_id = {location["id"]}'
        if 'interest' in arguments:
            cur.execute('SELECT id FROM interests WHERE name = %s', (arguments['interest'],))
            interest = cur.fetchone()
            if interest is None:
                errors.append('Invalid interest')
            else:
                baseRequest += f' AND id IN (SELECT user_id FROM users_interests WHERE interest_id = {interest["id"]})'
        orderBy = 'ORDER BY id ASC'
        if 'fame_rate' in arguments:
            if arguments['fame_rate']:
                orderBy = 'ORDER BY fame_rate DESC'
        blocked_filter = "AND users.id NOT IN (SELECT viewed_id FROM user_views WHERE viewer_id = %s AND blocked = TRUE UNION SELECT viewer_id FROM user_views WHERE viewed_id = %s AND blocked = TRUE)"
        cur.execute('SELECT id FROM users WHERE email = %s', (get_jwt_identity(),))
        user = cur.fetchone()
        if user is None:
            return jsonify({'error': 'User not found'})
        user = user['id']
        if 'show_blocks' in arguments and arguments['show_blocks'] == True:
            cur.execute(f'{baseRequest} {orderBy}', (get_jwt_identity(),))
        else:
            cur.execute(f'{baseRequest} {blocked_filter} {orderBy}', (get_jwt_identity(), user, user,))
        users = cur.fetchall()
        start = (page - 1) * profile_per_page
        end = start + profile_per_page
        for user in users[start:end]:
            research_results.append(convert_to_public_profile(user))
    max_page = len(users) // profile_per_page
    if len(users) % profile_per_page != 0:
        max_page += 1

    return jsonify({'success': True, 'result':research_results, 'max_page': max_page, 'page': page, 'profile_per_page': profile_per_page, 'errors': errors})

