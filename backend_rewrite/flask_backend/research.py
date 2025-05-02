from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db
from PIL import Image
import os

from .profiles_utils import convert_to_public_profile

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
        return jsonify({'success':False,'message': 'Missing parameters'})
    try:
        if isinstance(profile_per_page, str):
            profile_per_page = int(profile_per_page)
        if isinstance(page, str):
            page = int(page)
    except Exception as e:
        return jsonify({'success':False,'message': 'Invalid parameters'})
    if not isinstance(profile_per_page, int) or not isinstance(page, int):
        return jsonify({'success':False,'message': 'Invalid parameters'})
    if profile_per_page < 1 or page < 1:
        return jsonify({'success':False,'message': 'Invalid parameters'})
    arguments = {}
    errors = []
    try:
        if 'ageMin' in request.args:
            if type(request.args['ageMin']) is not str:
                errors.append('Invalid ageMin')
            else:
                if not request.args['ageMin'].isdigit():
                    errors.append('Invalid ageMin')
                else:
                    arguments['age_min'] = int(request.args['ageMin'])
        if 'ageMax' in request.args:
            if type(request.args['ageMax']) is not str:
                errors.append('Invalid ageMax')
            else:    
                if not request.args['ageMax'].isdigit():
                    errors.append('Invalid ageMax')
                else:
                    arguments['age_max'] = int(request.args['ageMax'])
        if 'location' in request.args:
            location = request.args['location']
            if type(location) is not str:
                errors.append('Invalid location')
            else:
                if not location or location == '':
                    pass
                else:
                    arguments['location'] = location
        if 'interest' in request.args:
            interest = request.args['interest']
            if type(interest) is not str:
                errors.append('Invalid interest')
            else:
                if not interest or interest == '':
                    pass
                else:
                    arguments['interest'] = interest
        if 'showBlocks' in request.args:
            show_blocks = request.args['showBlocks']
            if type(show_blocks) is not str:
                errors.append('Invalid showBlocks')
            else:
                if show_blocks not in ['true', 'false']:
                    errors.append('Invalid showBlocks')
                else:
                    if show_blocks == 'true':
                        arguments['show_blocks'] = True
                    else:
                        arguments['show_blocks'] = False
        if 'sortOrder' in request.args:
            sort_order = request.args['sortOrder']
            if sort_order not in ['ASC', 'DESC']:
                errors.append('Invalid sortOrder')
            else:
                arguments['sort_order'] = sort_order
        if 'sortBy' in request.args:
            sort_by = request.args['sortBy']
            if sort_by in ['common_interests', 'fame_rate', 'age', 'distance']:
                arguments['sort_by'] = sort_by
            else:
                errors.append('Invalid sortBy')
    except Exception as e:
        print("RESEARCH : failed arguments research", e)
        return jsonify({'success':False,'message': 'Invalid parameters'})
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email = %s', (get_jwt_identity(),))
        current_user = cur.fetchone()
        if current_user is None:
            return jsonify({'success':False,'message': 'User not found'})
        user_id = current_user['id']
        my_city_id = current_user['city_id']
        baseRequest = f"""
            {current_app.config["QUERIES"].get('-- get users')}
            WHERE u.id != %(user_id)s AND u.registration_complete = TRUE
            """
        params = {'user_id': user_id, 'city_id': my_city_id}
        if 'age_min' in arguments:
            baseRequest += ' AND u.age >= %(age_min)s'
            params.update({'age_min': arguments['age_min']})
        if 'age_max' in arguments:
            baseRequest += ' AND u.age <= %(age_max)s'
            params.update({'age_max': arguments['age_max']})
        if 'location' in arguments:
            from .cities import get_city_id
            city_id_requested = get_city_id(arguments['location'])
            if city_id_requested is None:
                errors.append('Invalid location')
            else:
                baseRequest += ' AND u.city_id = %(city_id_requested)s'
                params.update({'city_id_requested': city_id_requested})
        if 'interest' in arguments:
            cur.execute('SELECT id FROM interests WHERE name = %s', (arguments['interest'],))
            interest = cur.fetchone()
            if interest is None:
                errors.append('Invalid interest')
            else:
                baseRequest += f'''
                    AND u.id IN (
                        SELECT user_id FROM users_interests WHERE interest_id = %(interest_id)s
                    )
                '''
                params.update({'interest_id': interest['id']})
        if not arguments.get('show_blocks', False):
            baseRequest += '''
                AND u.id NOT IN (
                    SELECT viewed_id FROM user_views WHERE viewer_id = %(user_id)s AND blocked = TRUE
                    UNION
                    SELECT viewer_id FROM user_views WHERE viewed_id = %(user_id)s AND blocked = TRUE
                )
            '''
            params.update({'user_id': user_id})
        baseRequest += current_app.config["QUERIES"].get('-- group by users')
        sort_order = arguments.get('sort_order', 'DESC')
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'DESC'
        sort_by = arguments.get('sort_by', "")
        if sort_by not in ['common_interests', 'fame_rate', 'age', 'distance']:
            sort_by = 'id'
        if sort_by == 'common_interests':
            baseRequest += f' ORDER BY common_interests {sort_order}'
        elif sort_by == 'fame_rate':
            baseRequest += f' ORDER BY u.fame_rate {sort_order}'
        elif sort_by == 'age':
            baseRequest += f' ORDER BY u.age {sort_order}'
        elif sort_by == 'distance':
            baseRequest += f' ORDER BY distance {sort_order}'
        elif sort_by == 'id':
            baseRequest += f' ORDER BY u.id {sort_order}'
        cur.execute(baseRequest, params)
        u_max = cur.rowcount
        if u_max == 0:
            return jsonify({'success':True, 'result': [], 'max_page': 0, 'page': page, 'profile_per_page': profile_per_page, 'message': "No u found"})
        offset = (page - 1) * profile_per_page
        limit = profile_per_page
        baseRequest += f' OFFSET {offset} LIMIT {limit}'
        cur.execute(baseRequest, params)
        u = cur.fetchall()
        for user in u:
            research_results.append(convert_to_public_profile(user, current_user))
        max_page = u_max // profile_per_page
        if u_max % profile_per_page != 0:
            max_page += 1
    return jsonify({'success': True, 'result':research_results, 'max_page': max_page, 'page': page, 'profile_per_page': profile_per_page, 'message': " ,".join(errors) if errors else "All good"})

