import functools
import os
import json

from flask import Blueprint, jsonify, current_app
from .db import get_db


bp = Blueprint('get_informations', __name__, url_prefix='/api/getInformations')

@bp.route('/interests', methods=['GET'])
def get_interests_list():
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT * FROM interests')
            result = cur.fetchall()
            artCulture = []
            sport = []
            other = []
            for r in result:
                if r['category'] == 'artCulture':
                    artCulture.append(r['name'])
                elif r['category'] == 'sport':
                    sport.append(r['name'])
                else:
                    other.append(r['name'])
            interestsReturn = {
                'Culture': artCulture,
                'Sport': sport,
                'Other': other
            }
            return jsonify({'success':True, 'interests': interestsReturn})
    except Exception as e:
        print("GET INFORMATION ERROR : Failed to get interests list from database", e)
        return jsonify({'success': False, 'message': 'failed to get and parse interests'})

@bp.route('/register', methods=['GET'])
def get_register_info():
    return jsonify({'success': True, 'registerInfo': current_app.config['CONSTRAINTS']})