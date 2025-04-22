def upload_profile_picture():
    """Upload a profile picture for the user."""
    from flask import request, jsonify, current_app
    from .db import get_db
    from werkzeug.utils import secure_filename
    from flask_jwt_extended import get_jwt_identity
    import os
    # verifie si le fichier est bien present
    if 'picture' not in request.files:
        return jsonify({'success':False, 'error': 'No file part'})
    file = request.files['picture']
    if file.filename == '':
        return jsonify({'success':False, 'error': 'No selected file'})
    if file:
        db = get_db()
        user_email = get_jwt_identity()
        # on verifie si l'utilisateur existe et s'il a pas depasse le nombre max de photos de profil
        with db.cursor() as cur:
            cur.execute("SELECT pictures_number, id FROM users WHERE email = %s", (user_email,))
            result = cur.fetchone()
            if result is None:
                return jsonify({'success': False, 'error': 'User not found'})
            pictures_number = result["pictures_number"]
            user_id = result["id"]
            if pictures_number >= current_app.config['MAX_PICTURES']:
                return jsonify({'success': False, 'error': 'Maximum number of pictures reached'})
        # verification du type de fichier
        if allowed_file_extension(file.filename):
            # on le sauvegarde
            filename = f"{user_id}_{pictures_number}.{secure_filename(file.filename).rsplit('.', 1)[1].lower()}"
            file_path = os.path.join(current_app.config['PROFILE_PICTURES_DIR'], filename)
            file.save(file_path)
            # on verifie si l'image est corrompue
            if is_image_corrupted(file_path):
                os.remove(file_path)
                return jsonify({'success': False, 'error': 'Corrupted image'})
            # on incremente le nombre de photos de profil
            with db.cursor() as cur:
                cur.execute("UPDATE users SET pictures_number = pictures_number + 1 WHERE id = %s", (user_id,))
                db.commit()
            return jsonify({'success': True, 'filename': filename})

def get_profile_picture():
    """Get the profile pictures of the user indicated by the id."""
    from flask import jsonify, current_app, request, send_from_directory
    from .db import get_db
    user_id = request.args.get('user_id', None)
    photo_number = request.args.get('photo_number', None)
    if user_id is None or photo_number is None:
        return jsonify({'success': False, 'error': 'Missing parameters'})
    try:
        user_id = int(user_id)
        photo_number = int(photo_number)
    except Exception as e:
        return jsonify({'success': False, 'error': 'Invalid parameters'})
    if photo_number < 0 or photo_number >= current_app.config['MAX_PICTURES']:
        return jsonify({'success': False, 'error': 'Invalid photo number'})
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id, pictures_number FROM users WHERE id = %s", (user_id,))
        result = cur.fetchone()
        if result is None:
            return jsonify({'success': False, 'error': 'User not found'})
        filename = f"{user_id}_{photo_number}"
        file_path = current_app.config['PROFILE_PICTURES_DIR']
        result = find_file_without_extension(file_path, filename)
        if result is None:
            return jsonify({'success': False, 'error': 'File not found'})
        return send_from_directory(file_path, f"{filename}.{result.rsplit('.', 1)[1]}")
        
def delete_profile_picture():
    from flask import jsonify, request, current_app
    from flask_jwt_extended import get_jwt_identity
    from .db import get_db
    file_number = request.args.get('file_number', None)
    import os
    if file_number is None:
        return jsonify({'success': False, 'error': 'Missing parameters'})
    try:
        file_number = int(file_number)
    except Exception as e:
        return jsonify({'success': False, 'error': 'Invalid parameters'})
    if file_number < 0 or file_number >= current_app.config['MAX_PICTURES']:
        return jsonify({'success': False, 'error': 'Invalid photo number'})
    db = get_db()
    user_email = get_jwt_identity()
    with db.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if user is None:
            return jsonify({'success': False, 'error': 'User not found'})
    filename = f"{user['id']}_{file_number}"
    file_path = current_app.config['PROFILE_PICTURES_DIR']
    file = find_file_without_extension(file_path, filename)
    if file is None:
        return jsonify({'success': False, 'error': 'File not found'})
    os.remove(file)
    with db.cursor() as cur:
        cur.execute("UPDATE users SET pictures_number = pictures_number - 1 WHERE id = %s", (user["id"],))
        db.commit()
    realign_photos(user["id"], file_number)
    return jsonify({'success': True, 'message': 'File deleted successfully'})


    


def allowed_file_extension(filename):
    """Check if the file has an allowed extension."""
    from flask import current_app
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['IMAGE_EXTENSIONS']


def is_image_corrupted(image):
    from PIL import Image
    """Check if the image is corrupted."""
    try:
        img = Image.open(image)
        img.verify()
        return False
    except Exception as e:
        return True
    

def find_file_without_extension(directory, filename):
    """Find a file in a directory without its extension."""
    import os
    for file in os.listdir(directory):
        if file.startswith(filename + "."):  # Vérifie si le fichier commence par le bon nom
            return os.path.join(directory, file)
    return None


def realign_photos(user_id, file_number):
    """
    Modify the profile pictures name of the user to be in the right order.
    """
    from flask import current_app
    import os
    for i in range(file_number, 4):
        from .profiles_pictures_utils import find_file_without_extension
        old_file = find_file_without_extension(current_app.config['PROFILE_PICTURES_DIR'], f"{user_id}_{i+1}")
        if old_file is None:
            break
        new_file = os.path.join(current_app.config['PROFILE_PICTURES_DIR'], f"{user_id}_{i}.{old_file.split('.')[-1]}")
        os.rename(old_file, new_file)