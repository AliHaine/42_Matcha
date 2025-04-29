import json
import uuid
from flask import Blueprint, jsonify, request, current_app, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@bp.route('/upload_file', methods=['PUT'])
@jwt_required()
def upload_file():
        user_mail = get_jwt_identity()
        from .db import get_db
        db = get_db()
        with db.cursor() as cur:
            # Check if user exists
            cur.execute('SELECT id, status FROM users WHERE email = %s', (user_mail,))
            user = cur.fetchone()
            if not user:
                return jsonify({"success": False, "error": "User not found"})
            if user["status"] == False:
                return jsonify({"success": False, "error": "User is not active"})
            user_id = user['id']
        try:
            data = request.form.get('receiver_id', None)
            if data is None:
                return jsonify({"success": False, "error": "No data provided"})
            receiver_id = int(data)
        except Exception as e:
            return jsonify({"success": False, "error": "Invalid value for receiver_id"})
        # Check if receiver exists
        with db.cursor() as cur:
            cur.execute('SELECT id FROM users WHERE id = %s', (receiver_id,))
            receiver = cur.fetchone()
            if not receiver:
                return jsonify({"success": False, "error": "Receiver not found"})
        file = request.files.get('file', None)
        if file:
            try:
                with db.cursor() as cur:
                    cur.execute("SELECT created_at FROM messages WHERE sender_id = %s AND receiver_id = %s AND type = 'image' ORDER BY created_at DESC LIMIT 1", (user_id, receiver_id))
                    last_image = cur.fetchone()
                    time_required = timedelta(seconds=10)
                    if last_image:
                        last_image_time = last_image['created_at']
                        if datetime.now() - last_image_time < time_required:
                            return jsonify({"success": False, "error": "You can only send one image every minute"})
                if file.filename == '':
                    return jsonify({"success": False, "error": "No selected file"})
                if secure_filename(file.filename).split('.')[-1] not in current_app.config['IMAGE_EXTENSIONS']:
                    return jsonify({"success": False, "error": f"Invalid file format, only : {str(current_app.config['IMAGE_EXTENSIONS'])} is allowed"})
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = uuid.uuid4().hex[:8]
                filename = f"{user_id}-{timestamp}-{unique_id}.{secure_filename(file.filename).split('.')[-1]}"
                file_path = f"{current_app.config['BASE_DIR']}/uploads/chat"
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file.save(os.path.join(file_path, filename))
                from .profiles_pictures_utils import is_image_corrupted
                if is_image_corrupted(os.path.join(file_path, filename)):
                    os.remove(os.path.join(file_path, filename))
                    return jsonify({"success": False, "error": "Image is corrupted"})
                with db.cursor() as cur:
                    cur.execute("INSERT INTO messages (sender_id, receiver_id, message, type) VALUES (%s, %s, %s, %s)",
                                (user_id, receiver_id, filename, "image"))
                    db.commit()
                    from .websocket import send_message
                    arguments = {
                        "message": filename,
                        "type": "image",
                        "author_id": user_id,
                        "created_at": datetime.now().strftime('%H:%M'),
                    }
                    send_message(arguments=arguments, rooms=[f"user_{receiver_id}", f"user_{user_id}"])
                return jsonify({"success": True})
            except Exception as e:
                print("CHAT FAIL : Failed to save file", e)
                return jsonify({"success": False, "error": "An error occurred while saving the file"})
        else:
            return jsonify({"success": False, "error": "No file provided"})
 

@bp.route('/recover_image', methods=['GET'])
@jwt_required()
def recover_image():
    user_mail = get_jwt_identity()
    from .db import get_db
    db = get_db()
    with db.cursor() as cur:
        # Check if user exists
        cur.execute('SELECT id, status FROM users WHERE email = %s', (user_mail,))
        user = cur.fetchone()
        if not user:
            return jsonify({"success": False, "error": "User not found"})
        if user["status"] == False:
            return jsonify({"success": False, "error": "User is not active"})
        user_id = user['id']
    try:
        image_name = request.args.get('image_name', None)
        if image_name is None:
            return jsonify({"success": False, "error": "No data provided"})
    except Exception as e:
        return jsonify({"success": False, "error": "Invalid value for image_name"})
    file_path = f"{current_app.config['BASE_DIR']}/uploads/chat"
    if os.path.exists(os.path.join(file_path, image_name)):
        return send_file(os.path.join(file_path, image_name))
    else:
        return jsonify({"success": False, "error": "File not found"})