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
    try:
        if 'age_min' in request.args:
            arguments['age_min'] = int(request.args['age_min'])
        if 'age_max' in request.args:
            arguments['age_max'] = int(request.args['age_max'])
        if 'location' in request.args:
            arguments['location'] = request.args['location']
        if 'interests' in request.args:
            arguments['interests'] = request.args['interests']
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
            cur.execute('SELECT id FROM locations WHERE name = %s', (arguments['location'],))
            location = cur.fetchone()
            if location is None:
                return jsonify({'success': True, 'result':research_results})
            baseRequest += f' AND location_id = {location["id"]}'
        if 'interests' in arguments:
            interests = arguments['interests'].split(',')
            for interest in interests:
                cur.execute('SELECT id FROM interests WHERE name = %s', (interest,))
                interest = cur.fetchone()
                if interest is None:
                    return jsonify({'success': True, 'result':research_results})
                baseRequest += f' AND id IN (SELECT user_id FROM user_interests WHERE interest_id = {interest["id"]})'
        cur.execute(f'{baseRequest} ORDER BY id ASC', (get_jwt_identity(),))
        users = cur.fetchall()
        start = (page - 1) * profile_per_page
        end = start + profile_per_page
        for user in users[start:end]:
            research_results.append(convert_to_public_profile(user))
    max_page = len(users) // profile_per_page
    if len(users) % profile_per_page != 0:
        max_page += 1

    return jsonify({'success': True, 'result':research_results, 'max_page': max_page, 'page': page})

