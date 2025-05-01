
def export_constraints(app, cur):
    import re
    """
    Exporte les contraintes de la table "users" dans le fichier de configuration de l'application.
    """
    table_names = ["users", "user_views"]
    columns_names = {
        "searching", "commitment", "frequency", "weight", "size", "shape",
        "smoking", "alcohol", "diet", "firstname", "lastname", "description", "username",
        "reason"
    }
    constraints = {}

    query = """
    SELECT pg_get_constraintdef(oid) as constraint_def 
    FROM pg_constraint 
    WHERE contype = 'c' 
    AND conrelid = %s::regclass;
    """
    for table_name in table_names:
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
                    match = regex_pattern.search(constraint_def)
                    if match:
                        if match.group("values"):
                            raw_values = match.group("values").split(", ")
                            values = []
                            for v in raw_values:
                                # Nettoyage de chaque valeur : on enlève les ::, les parenthèses et les apostrophes
                                clean = re.sub(r"::.*", "", v)  # supprime tout ce qui suit "::"
                                clean = clean.strip(" '()")     # supprime les ' ( ) et espaces autour
                                if clean == "": 
                                    continue
                                values.append(clean)
                            constraints[column] = values

                        elif match.group("regex"):
                            # On remplace les doubles backslashes par un simple (il y en a 4 et 2 dans le replace car il faut echapper le backslash)
                            constraints[column] = match.group("regex").replace("\\\\", "\\")

    app.config['CONSTRAINTS'] = constraints
    print("INIT : Constraints loaded successfully")

def load_queries(app, query_file):
    """
    Charge les requêtes SQL à partir d'un fichier et les retourne sous forme de dictionnaire.
    Chaque requête doit être séparée par un point-virgule et commencer par un commentaire definisant son nom.
    """
    queries_dict = {}
    try:
        with open(query_file, "r", encoding="utf-8") as f:
            queries = f.read().split(";")  # Séparer les requêtes s'il y en a plusieurs
            # queries_dict = {q.split("\n")[0]: q for q in queries if q.strip()}
            for q in queries:
                if not q.strip():
                    continue
                stripped_query = q.strip().split("\n")
                if stripped_query:
                    # On prend le premier commentaire comme nom de la requête
                    name = stripped_query[0].strip()
                    # On enlève le commentaire du début
                    query = "\n".join(stripped_query[1:]).strip()
                    queries_dict[name] = query

        print("INIT : Queries loaded successfully")
    except Exception as e:
        print(f"INIT FAIL : Failed to load queries from {query_file}: {e}")
    app.config['QUERIES'] = queries_dict

def load_common_passwords(app, file_path):
    """
    charge un dictionnaire de mots de passe communs à partir d'un fichier et les stocke dans la configuration de l'application.
    Le fichier doit contenir un mot de passe par ligne.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        # Remove duplicates and empty lines
        common_passwords = set(filter(None, (line.strip().lower() for line in lines if line.strip() and len(line.strip()) >= 5)))
        print("INIT : Common passwords loaded successfully")
    except Exception as e:
        print(f"INIT FAIL : Failed to load common passwords from {file_path}: {e}")
        common_passwords = set()
    app.config['COMMON_PASSWORDS'] = common_passwords

def set_interests_list(app, cur):
    """
    Charge la liste des centres d'intérêt à partir de la base de données et les stocke dans la configuration de l'application.
    """
    try:
        cur.execute('SELECT name FROM interests')
        result = cur.fetchall()
        app.config['AVAILABLE_INTERESTS'] = [r['name'] for r in result]
        print("INIT : Interests list loaded successfully")
    except Exception as e:
        print("INIT FAIL : Failed to get interests list from database", e)
        app.config['AVAILABLE_INTERESTS'] = []

def reset_active_connections(cur):
    """
    Réinitialise le nombre de connexions actives pour tous les utilisateurs.
    """
    try:
        cur.execute('UPDATE users SET active_connections = 0, status = FALSE WHERE status = TRUE')
        cur.connection.commit()
        print("INIT : Active connections reset successfully")
    except Exception as e:
        print("Failed to reset active connections", e)

def create_paths(app):
    import os
    """
    Crée les répertoires nécessaires pour le stockage des fichiers.
    """
    try:
        if not os.path.exists(app.config['PROFILE_PICTURES_DIR']):
            os.makedirs(app.config['PROFILE_PICTURES_DIR'])
        if not os.path.exists(app.config['CHAT_UPLOAD_DIR']):
            os.makedirs(app.config['CHAT_UPLOAD_DIR'])
        print("INIT : Paths created successfully")
    except Exception as e:
        print("Failed to create paths", e)

def init_mail_server(app):
    from flask_mail import Mail
    """
    Initialise le serveur de mail.
    """
    try:
        if app.config['MAIL_USERNAME'] == '' or app.config['MAIL_PASSWORD'] == '':
            print("INIT : Mail server not initialized : No credentials provided")
            app.config['MAIL'] = None
        else:
            mail = Mail(app)
            app.config['MAIL'] = mail
            print("INIT : Mail server initialized successfully")
    except Exception as e:
        print("INIT FAIL : Failed to initialize mail server", e)
        app.config['MAIL'] = None

def register_blueprints(app):
    """
    Enregistre les blueprints de l'application.
    """
    from . import auth
    from . import profiles
    from . import research
    from . import matcha
    from . import get_informations
    from . import chat
    try:
        app.register_blueprint(auth.bp)
        app.register_blueprint(profiles.bp)
        app.register_blueprint(research.bp)
        app.register_blueprint(matcha.bp)
        app.register_blueprint(get_informations.bp)
        app.register_blueprint(chat.bp)
    except Exception as e:
        print("INIT FAIL : Failed to register blueprints", e)
        raise e
    print("INIT : Blueprints registered successfully")
