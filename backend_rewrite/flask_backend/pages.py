from flask import Blueprint, jsonify, request, current_app

bp = Blueprint('pages', __name__, url_prefix='/api/pages')

@bp.route('/<string:page_name>', methods=['GET'])
def get_page(page_name):
    """
    Get the content of a page by its name.
    """
    # Define the path to the pages directory
    pages_dir = current_app.config['PAGES_DIR']
    
    # Construct the full path to the requested page
    page_path = f"{pages_dir}/{page_name}.txt"
    
    try:
        # Open and read the content of the page
        with open(page_path, 'r') as file:
            content = file.read()
        return jsonify({'success': True, 'content': content})
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Page not found'})
