from flask_socketio import SocketIO
import sys
socketio = SocketIO(cors_allowed_origins="*")

sys.setdefaultencoding('utf-8') if hasattr(sys, 'setdefaultencoding') else None

def create_app(test_config=None):
    """
    Crée et configure l'application Flask.
    """
    from flask import Flask, jsonify
    from flask_cors import CORS
    from datetime import timedelta
    from dotenv import load_dotenv
    from . import db
    from .__init__utils import (
        load_queries,
        load_common_passwords,
        set_interests_list,
        export_constraints,
        reset_active_connections,
        create_paths,
        init_mail_server,
        register_blueprints
    )
    import os
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {
        "origins": ["http://localhost:4200", "http://127.0.0.1:4200"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }})
    # environment setup
    base_dir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv()
    load_dotenv(dotenv_path=os.path.join(base_dir, '../../settings/.flask.env'))
    load_dotenv(dotenv_path=os.path.join(base_dir, '../../settings/.database.env'))
    # load configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', default='dev'),
        DEBUG=os.getenv('DEBUG', default='False') == 'True',
        # database configuration
        DATABASE_HOST=os.getenv('POSTGRES_HOST', default='localhost'),
        DATABASE_USER=os.getenv('POSTGRES_USER', default='admin'),
        DATABASE_PASSWORD=os.getenv('POSTGRES_PASSWORD', default='admin'),
        DATABASE=os.getenv('POSTGRES_DB', default='matcha'),
        DATABASE_PORT=os.getenv('POSTGRES_PORT', default='5432'),
        # JWT configuration
        JWT_BLACKLIST_ENABLED=True,
        JWT_BLACKLIST_TOKEN_CHECKS=['access'],
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
        # path configuration
        BASE_DIR=base_dir,
        PROFILE_PICTURES_DIR=os.path.join(base_dir, 'uploads/profile_pictures'),
        CHAT_UPLOAD_DIR=os.path.join(base_dir, 'uploads/chat'),
        # file configuration
        IMAGE_EXTENSIONS=['png', 'jpg', 'jpeg'],
        MAX_CONTENT_LENGTH=25 * 1024 * 1024,
        MAX_PICTURES=5,
        # mail configuration
        MAIL_SERVER=os.getenv('MAIL_SERVER', default='smtp.gmail.com'),
        MAIL_PORT=os.getenv('MAIL_PORT', default=587),
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME', default=''),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', default=''),
        # other configuration
        JSON_AS_ASCII=False,
        SOCKETIO_INSTANCE=socketio,
        USE_RELOADER=os.getenv('USE_RELOADER', default='False') == 'True',   
    )
    try:
        with app.app_context():
            if 'init-db' in sys.argv:
                db.init_app(app)
                return app
            # setting up the default configuration of services elements
            database = db.get_db()
            with database.cursor() as cur:
                set_interests_list(app, cur)
                export_constraints(app, cur)
                reset_active_connections(cur)
            load_queries(app, os.path.join(app.config['BASE_DIR'], 'queries.sql'))
            load_common_passwords(app, os.path.join(app.config['BASE_DIR'], 'common_passwords.txt'))
            create_paths(app)
            init_mail_server(app)
            register_blueprints(app)
            jwt_setup(app)
            socketio_setup(app)
            @app.route('/health', methods=['GET'])
            def health():
                """
                Endpoint de vérification de l'état de l'application.
                """
                return jsonify({'status': 'ok'}), 200
        return app
    except Exception as e:
        print("Init server failed, stopping", e)
        raise e

def socketio_setup(app):
    try:
        from . import websocket
        socketio.init_app(app, async_mode='eventlet')
        print("INIT : SocketIO setup successfully")
    except Exception as e:
        print("INIT FAIL : Failed to setup socketio", e)
        raise e

def jwt_setup(app):
    """
    Configure le JWT pour l'application Flask.
    """
    from flask_jwt_extended import JWTManager
    from .jwt_handler import (
        missing_token_callback,
        expired_token_callback,
        invalid_token_callback,
        revoked_token_callback
    )
    try:
        jwt = JWTManager(app)
        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header, jwt_payload):
            from .auth import BLACKLIST
            return jwt_payload["jti"] in BLACKLIST
        app.config['JWT_BLACKLIST_ENABLED'] = True
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
        # Callbacks for JWT errors
        jwt.unauthorized_loader(missing_token_callback)
        jwt.expired_token_loader(expired_token_callback)
        jwt.invalid_token_loader(invalid_token_callback)
        jwt.revoked_token_loader(revoked_token_callback)
        print("INIT : JWT setup successfully")
    except Exception as e:
        print("INIT FAIL : Failed to setup JWT", e)