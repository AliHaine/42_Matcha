import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from datetime import timedelta

from .jwt_handler import missing_token_callback, expired_token_callback, invalid_token_callback, revoked_token_callback

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DATABASE_HOST='localhost',
        DATABASE_USER='admin',
        DATABASE_PASSWORD='admin/0123456789',
        DATABASE='matcha',
        DATABASE_PORT=6000,
        JWT_BLACKLIST_ENABLED=True,
        JWT_BLACKLIST_TOKEN_CHECKS=['access'],
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
    )

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

    from . import db
    db.init_app(app)

    from . import auth
    from . import profiles
    app.register_blueprint(auth.bp)
    app.register_blueprint(profiles.bp)

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

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"],
                                        "methods": ["GET", "POST"],
                                        "allow_headers": ["Content-Type", "Authorization"]
                                        }}, supports_credentials=True)
    return app