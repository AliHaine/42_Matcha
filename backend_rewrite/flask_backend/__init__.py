import os
import re

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flask_socketio import SocketIO

from flask_mail import Mail, Message

from .db import get_db
from datetime import timedelta

import sys

from .jwt_handler import missing_token_callback, expired_token_callback, invalid_token_callback, revoked_token_callback

socketio = SocketIO(cors_allowed_origins="*")

sys.setdefaultencoding('utf-8') if hasattr(sys, 'setdefaultencoding') else None

import re

def export_constraints(app, cur):
    table_name = "users"
    columns_names = {
        "searching", "commitment", "frequency", "weight", "size", "shape",
        "smoking", "alcohol", "diet", "firstname", "lastname", "description", "username"
    }
    constraints = {}

    query = """
    SELECT pg_get_constraintdef(oid) as constraint_def 
    FROM pg_constraint 
    WHERE contype = 'c' 
    AND conrelid = %s::regclass;
    """
    
    cur.execute(query, (table_name,))
    results = cur.fetchall()

    regex_pattern = re.compile(r"""
        ARRAY\[(?P<values>[^\]]+)\]        # Capture ARRAY[...] (list of values)
        |                                  # OR
        [~|SIMILAR TO]\s+'(?P<regex>.*?)'  # Capture regex constraint
    """, re.VERBOSE)

    for row in results:
        constraint_def = row["constraint_def"]
        
        for column in columns_names:
            if column in constraint_def:
                print(f"Constraint found for column {column}: {constraint_def}")
                match = regex_pattern.search(constraint_def)
                if match:
                    if match.group("values"):
                        raw_values = match.group("values").split(", ")
                        values = []
                        for v in raw_values:
                            # Nettoyage de chaque valeur : on enlève les ::, les parenthèses et les apostrophes
                            clean = re.sub(r"::.*", "", v)  # supprime tout ce qui suit "::"
                            clean = clean.strip(" '()")     # supprime les ' ( ) et espaces autour
                            values.append(clean)
                        constraints[column] = values

                    elif match.group("regex"):
                        constraints[column] = match.group("regex").replace("\\\\", "\\")

    app.config['CONSTRAINTS'] = constraints
    # for constraint in constraints:
    #     print(f"Constraint for {constraint}: {constraints[constraint]}")

def load_queries(query_file):
    with open(query_file, "r", encoding="utf-8") as f:
        queries = f.read().split(";")  # Séparer les requêtes s'il y en a plusieurs
        return {q.split("\n")[0]: q for q in queries if q.strip()}

def init_cities():
    from .db import get_db
    database = get_db()
    with database.cursor() as cur:
        cur.execute('SELECT * FROM cities')
        result = cur.fetchall()
        if len(result) == 0:
            from .cities import get_city_id
            get_city_id({'lat': 47.75, 'lon': 7.3})

def load_common_passwords(app, file_path):
    print("Loading common passwords from file:", file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    # Remove duplicates and empty lines
    common_passwords = set(filter(None, (line.strip().lower() for line in lines if line.strip())))    # Store the list in the app config
    app.config['COMMON_PASSWORDS'] = common_passwords

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {
        "origins": ["http://localhost:4200", "http://127.0.0.1:4200"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
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
        IMAGE_EXTENSIONS=['png', 'jpg', 'jpeg'],
        JSON_AS_ASCII=False,
        SOCKETIO_INSTANCE=socketio,
        MAIL_SERVER=os.getenv('MAIL_SERVER', default='smtp.gmail.com'),
        MAIL_PORT=os.getenv('MAIL_PORT', default=587),
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME', default=''),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', default=''),
        MAX_CONTENT_LENGTH=25 * 1024 * 1024,
    )
    with app.app_context():
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
                app.config["QUERIES"] = load_queries(os.path.join(app.config['BASE_DIR'], 'queries.sql'))
                try:
                    load_common_passwords(app, os.path.join(app.config['BASE_DIR'], 'common_passwords.txt'))
                except Exception as e:
                    print("Failed to load common passwords file", e)
                    app.config['COMMON_PASSWORDS'] = []
        except Exception as e:
            print("INIT ERROR : Failed to get interests list from database", e)
            app.config['AVAILABLE_INTERESTS'] = []
            print("INIT ERROR : Did you initialize the database ?")

        # ensure the instance folder exists
        try:
            if not os.path.exists(app.instance_path):
                os.makedirs(app.instance_path)
            if not os.path.exists(app.config['PROFILE_PICTURES_DIR']):
                os.makedirs(app.config['PROFILE_PICTURES_DIR'])
        except Exception as e:
            print("Failed to create path", e)
        try:
            if app.config['MAIL_USERNAME'] == '' or app.config['MAIL_PASSWORD'] == '':
                print("Mail server not initialized : No credentials provided")
                app.config['MAIL'] = None
            else:
                mail = Mail(app)
                app.config['MAIL'] = mail
        except Exception as e:
            print("Failed to initialize mail server", e)


        # registering blueprints (routes)
        from . import auth
        from . import profiles
        from . import research
        from . import matcha
        from . import get_informations
        from . import chat
        app.register_blueprint(auth.bp)
        app.register_blueprint(profiles.bp)
        app.register_blueprint(research.bp)
        app.register_blueprint(matcha.bp)
        app.register_blueprint(get_informations.bp)
        app.register_blueprint(chat.bp)

        @app.route('/test')
        def test():
            msg = Message("Hello",sender=app.config["MAIL_USERNAME"],recipients=[""])
            msg.body = "testing"
            mail.send(msg)
            return "Hello, World !"
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
        
        from . import websocket
        
        socketio.init_app(app, async_mode='eventlet')
    return app

