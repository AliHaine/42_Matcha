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
        return jsonify({'error': 'Missing parameters'}), 400
    try:
        if isinstance(profile_per_page, str):
            profile_per_page = int(profile_per_page)
        if isinstance(page, str):
            page = int(page)
    except Exception as e:
        return jsonify({'error': 'Invalid parameters'}), 400
    if profile_per_page < 1 or page < 1:
        return jsonify({'error': 'Invalid parameters'}), 400
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email != %s AND registration_complete = TRUE ORDER BY id ASC', (get_jwt_identity(),))
        users = cur.fetchall()
        start = (page - 1) * profile_per_page
        end = start + profile_per_page
        for user in users[start:end]:
            research_results.append(convert_to_public_profile(user))
    return jsonify({'success': True, 'result':research_results}), 200

