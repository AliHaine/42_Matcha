import os
import re

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flask_socketio import SocketIO

from .db import get_db
from datetime import timedelta

import sys

from .jwt_handler import missing_token_callback, expired_token_callback, invalid_token_callback, revoked_token_callback

socketio = SocketIO(cors_allowed_origins="*")
from . import websocket

sys.setdefaultencoding('utf-8') if hasattr(sys, 'setdefaultencoding') else None

def export_constraints(app, cur):
    table_name = "users"
    columns_names = ["searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet", 'firstname', 'lastname', "description"]
    constraints = {}

    # Requête pour récupérer la définition de la contrainte CHECK
    query = f"""
    SELECT pg_get_constraintdef(oid) 
    FROM pg_constraint 
    WHERE contype = 'c' 
    AND conrelid = %s::regclass
    AND pg_get_constraintdef(oid) LIKE %s;
    """
    for column_name in columns_names:
        cur.execute(query, (table_name, f'%{column_name}%'))
        results = cur.fetchall()
        for result in results:
            if result:
                constraint_def = result["pg_get_constraintdef"]
                match = re.search(r'ARRAY\[(.*?)\]', constraint_def)
                if match:
                    values = match.group(1).split(", ")
                    values = [re.sub(r"::.*", "", v.replace("'", "").strip()) for v in values]
                    constraints[column_name] = values
                match_regex = re.search(r"[~|SIMILAR TO]\s+'(.*?)'", constraint_def)
                if match_regex:
                    extracted_regex = match_regex.group(1)
                    extracted_regex = extracted_regex.replace("\\\\", "\\")
                    constraints[column_name] = extracted_regex
    app.config['CONSTRAINTS'] = constraints


def init_cities():
    from .db import get_db
    database = get_db()
    with database.cursor() as cur:
        cur.execute('SELECT * FROM cities')
        result = cur.fetchall()
        if len(result) == 0:
            from .cities import get_city_id
            get_city_id({'lat': 47.75, 'lon': 7.3})

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:4200", "http://127.0.0.1:4200", "*"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Ajout de OPTIONS
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})
    # load dotenv file
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../settings/.flask.env'))
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../settings/.database.env'))
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', default='dev'),
        DATABASE_HOST=os.getenv('POSTGRES_HOST', default='localhost'),
        DATABASE_USER=os.getenv('POSTGRES_USER', default='admin'),
        DATABASE_PASSWORD=os.getenv('POSTGRES_PASSWORD', default='admin'),
        DATABASE=os.getenv('POSTGRES_DB', default='matcha'),
        DATABASE_PORT=os.getenv('POSTGRES_PORT', default='5432'),
        JWT_BLACKLIST_ENABLED=True,
        JWT_BLACKLIST_TOKEN_CHECKS=['access'],
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
        BASE_DIR=os.path.dirname(os.path.abspath(__file__)),
        PROFILE_PICTURES_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads/profile_pictures'),
        PROFILE_PIC_EXTENSIONS=['png', 'jpg', 'jpeg'],
        JSON_AS_ASCII=False,
        SOCKETIO_INSTANCE=socketio,
    )
    app.app_context().push()
    # initialize the database
    if 'init-db' in sys.argv:
        from . import db
        db.init_app(app)
        return app
    try:
        database = get_db()
        with database.cursor() as cur:
            cur.execute('SELECT name FROM interests')
            result = cur.fetchall()
            app.config['AVAILABLE_INTERESTS'] = [r['name'] for r in result]
            export_constraints(app, cur)
            cur.execute('UPDATE users SET active_connections = 0, status = FALSE WHERE status = TRUE')
            database.commit()
            init_cities()
    except Exception as e:
        print("Failed to get interests list from database", e)
        app.config['AVAILABLE_INTERESTS'] = []
        print("Did you initialize the database ?\n\n")
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # registering blueprints (routes)
    from . import auth
    from . import profiles
    from . import research
    from . import matcha
    from . import get_informations
    app.register_blueprint(auth.bp)
    app.register_blueprint(profiles.bp)
    app.register_blueprint(research.bp)
    app.register_blueprint(matcha.bp)
    app.register_blueprint(get_informations.bp)

    @app.route('/test')
    def hello():
        from .cities import get_city_around
        return str(get_city_around(1, 50))

    # registering jwt and its callbacks
    jwt = JWTManager(app)
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        from .auth import BLACKLIST
        return jwt_payload["jti"] in BLACKLIST
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    jwt.unauthorized_loader(missing_token_callback)
    jwt.expired_token_loader(expired_token_callback)
    jwt.invalid_token_loader(invalid_token_callback)
    jwt.revoked_token_loader(revoked_token_callback)
    socketio.init_app(app, async_mode='eventlet')
    return app

