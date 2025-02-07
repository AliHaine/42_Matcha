import functools
import os
import json

from flask import Blueprint, request, jsonify, current_app
from .db import get_db

from .decorators import registration_completed

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
            interestsReturn = []
            interestsReturn.append(artCulture)
            interestsReturn.append(sport)
            interestsReturn.append(other)
            return jsonify({'success':True, 'interests': interestsReturn})
    except Exception as e:
        print("Failed to get interests list from database", e)
        return jsonify({'success':False, 'error': 'failed to get and parse interests'})