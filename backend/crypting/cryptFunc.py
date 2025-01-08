from flask_bcrypt import Bcrypt


bcrypt = None

def init_bcrypt(app):
    global bcrypt
    if app is None:
        raise Exception('Flask app not provided')
    if bcrypt is None:
        bcrypt = Bcrypt(app)

def crypt_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)