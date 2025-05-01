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
    if profile_per_page < 1 or page < 1:
        return jsonify({'success':False,'message': 'Invalid parameters'})
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
            location = request.args['location']
            if not location or location == '':
                pass
            else:
                arguments['location'] = location
        if 'interest' in request.args:
            interest = request.args['interest']
            if not interest or interest == '':
                pass
            else:
                arguments['interest'] = interest
        if 'showBlocks' in request.args:
            show_blocks = request.args['showBlocks']
            if show_blocks == 'true':
                arguments['show_blocks'] = True
            elif show_blocks == 'false':
                arguments['show_blocks'] = False
            else:
                errors.append('Invalid showBlocks')
        if 'sortOrder' in request.args:
            sort_order = request.args['sortOrder']
            if sort_order == 'ASC' or sort_order == 'DESC':
                arguments['sort_order'] = sort_order
            else:
                errors.append('Invalid sortOrder')
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
        baseRequest = '''
            SELECT 
                users.*,
                COUNT(DISTINCT common.interest_id) AS common_interests,
                ST_Distance(user_city.geom::geography, my_city.geom::geography) AS distance
            FROM users
            JOIN cities user_city ON users.city_id = user_city.id
            JOIN cities my_city ON my_city.id = %s
            LEFT JOIN users_interests other ON other.user_id = users.id
            LEFT JOIN users_interests common 
                ON common.interest_id = other.interest_id AND common.user_id = %s
            WHERE users.id != %s AND users.registration_complete = TRUE
        '''
        params = [my_city_id, user_id, user_id]
        if 'age_min' in arguments:
            baseRequest += f' AND users.age >= %s'
            params.append(arguments['age_min'])
        if 'age_max' in arguments:
            baseRequest += f' AND users.age <= %s'
            params.append(arguments['age_max'])
        if 'location' in arguments:
            cur.execute('SELECT id FROM cities WHERE cityname = %s', (arguments['location'],))
            location = cur.fetchone()
            if location is None:
                errors.append('Invalid location')
            else:
                baseRequest += f' AND users.city_id = %s'
                params.append(location['id'])
        if 'interest' in arguments:
            cur.execute('SELECT id FROM interests WHERE name = %s', (arguments['interest'],))
            interest = cur.fetchone()
            if interest is None:
                errors.append('Invalid interest')
            else:
                baseRequest += f'''
                    AND users.id IN (
                        SELECT user_id FROM users_interests WHERE interest_id = %s
                    )
                '''
                params.append(interest['id'])
        if not arguments.get('show_blocks', False):
            baseRequest += '''
                AND users.id NOT IN (
                    SELECT viewed_id FROM user_views WHERE viewer_id = %s AND blocked = TRUE
                    UNION
                    SELECT viewer_id FROM user_views WHERE viewed_id = %s AND blocked = TRUE
                )
            '''
            params.extend([user_id, user_id])
        baseRequest += ' GROUP BY users.id, user_city.geom, my_city.geom'
        sort_order = arguments.get('sort_order', 'DESC')
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'DESC'
        sort_by = arguments.get('sort_by', "")
        if sort_by not in ['common_interests', 'fame_rate', 'age', 'distance']:
            sort_by = 'id'
        if sort_by == 'common_interests':
            baseRequest += f' ORDER BY common_interests {sort_order}'
        elif sort_by == 'fame_rate':
            baseRequest += f' ORDER BY users.fame_rate {sort_order}'
        elif sort_by == 'age':
            baseRequest += f' ORDER BY users.age {sort_order}'
        elif sort_by == 'distance':
            baseRequest += f' ORDER BY distance {sort_order}'
        elif sort_by == 'id':
            baseRequest += f' ORDER BY users.id {sort_order}'
        users = cur.fetchall()
        # start = (page - 1) * profile_per_page
        # end = start + profile_per_page
        offset = (page - 1) * profile_per_page
        limit = profile_per_page
        baseRequest += f' OFFSET {offset} LIMIT {limit}'
        cur.execute(baseRequest, tuple(params))
        users = cur.fetchall()
        for user in users:
            research_results.append(convert_to_public_profile(user, current_user))
        cur.execute('SELECT COUNT(*) FROM users WHERE id != %s AND registration_complete = TRUE', (user_id,))
        count = cur.fetchone()
        max_page = count['count'] // profile_per_page
        if count['count'] % profile_per_page != 0:
            max_page += 1
    return jsonify({'success': True, 'result':research_results, 'max_page': max_page, 'page': page, 'profile_per_page': profile_per_page, 'message': " ,".join(errors) if errors else "All good"})

