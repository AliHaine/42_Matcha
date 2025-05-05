from .db import get_db
from .cities import get_city_id
import re
from flask_jwt_extended import jwt_required, get_jwt_identity
# ALLOWED_CHARACTERS_BASE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"
REGEX_ALLOWED_CHARACTERS_BASE = r'^[a-zA-Z-]+$'
from flask import current_app

def dynamic_regex(digits=False, special=False, accents=False, spaces=False):
    base_chars = "a-zA-Z"  # Lettres de base
    regex = "^[" + base_chars

    if digits:
        regex += "0-9"
    if special:
        regex += re.escape("-@!$#%&*")  # Ajoute des caractères spéciaux sécurisés
    if accents:
        regex += "À-ÖØ-öø-ÿ"  # Évite les caractères indésirables comme × et ÷
    if spaces:
        regex += " "

    regex += "]+$"
    return regex

def generate_email_token(email: str = "", system: str = "") -> str:
    import random
    import string
    from .db import get_db
    db = get_db()
    # reset = reset_password
    # confirm = confirm_email
    if system not in ["reset", "confirm"]:
        return None
    with db.cursor() as cur:
        # Générer un token aléatoire de 64 caractères
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        # Vérifier si le token existe déjà dans la base de données
        while True:
            cur.execute('SELECT * FROM users WHERE email_token = %s OR reset_token = %s', (token, token,))
            if cur.fetchone() is None:
                break
            else:
                # Générer un nouveau token aléatoire si le token existe déjà
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        if system == "reset":
            from datetime import datetime, timedelta
            expiration_duration = timedelta(minutes=15)
            expires_at = datetime.now() + expiration_duration
            cur.execute('UPDATE users SET reset_token = %s, expiration = %s WHERE email = %s', (token, expires_at, email,))
        elif system == "confirm":
            cur.execute('UPDATE users SET email_token = %s WHERE email = %s', (token, email))
    db.commit()
    return token


FIELDS_UPDATABLE = ["firstname", "lastname", "username", "email", "password", "age", "gender", "city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet", "description", "interests", "hetero"]
STEP1_FIELDS = ["username", "firstname", "lastname", "email", "password", "age", "gender", "hetero"]
STEP2_FIELDS = ["city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet"]
STEP3_FIELDS = ["interests", "description"]
def create_user(user_informations):
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                'INSERT INTO users (firstname, lastname, email, password, age, gender, username, hetero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (user_informations['firstname'], user_informations['lastname'], user_informations['email'], user_informations['password'], user_informations['age'], user_informations['gender'], user_informations['username'], user_informations['hetero'])
            )
        db.commit()
        return True
    except Exception as e:
        print("CREATE USER FAIL : ", e)
        return False

def update_interests(interests, user_email):
    for interest in interests:
        if interest not in current_app.config['AVAILABLE_INTERESTS']:
            return False
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT id FROM users WHERE email = %s', (user_email,))
            user = cur.fetchone()
            if user is None:
                return False
            user_id = user['id']
            cur.execute('DELETE FROM users_interests WHERE user_id = %s', (user_id,))
            for interest in interests:
                cur.execute('SELECT id FROM interests WHERE name = %s', (interest,))
                interest_id = cur.fetchone()['id']
                cur.execute('INSERT INTO users_interests (user_id, interest_id) VALUES (%s, %s)', (user_id, interest_id))
        db.commit()
        return True
    except Exception as e:
        print("UPDATE INTEREST FAIL : error :", e)
        return False

def update_user_fields(user_informations, user_email):
    if not isinstance(user_informations, dict):
        return False
    if not isinstance(user_email, str):
        return False
    if len(user_email) == 0:
        return False
    try:
        values = []
        for key, value in user_informations.items():
            if key in FIELDS_UPDATABLE:
                values.append(value)
            else:
                raise Exception(f"Invalid field {key}")
        db = get_db()
        with db.cursor() as cur:
            values_name = ""
            values_content = tuple()
            for key, value in user_informations.items():
                if key in FIELDS_UPDATABLE:
                    if key == "city":
                        city_id = get_city_id(value)
                        if city_id is None:
                            return False
                        values_name += f"city_id = %s, "
                        values_content += (city_id,)
                    elif key == "interests":
                        res = update_interests(value, user_email)
                        if res == False:
                            return False
                    else:
                        values_name += f"{key} = %s, "
                        values_content += (value,)
            values_name = values_name[:-2]
            values_content += (user_email,)
            cur.execute(
                'UPDATE users SET '+ values_name + ' WHERE email = %s',
                values_content
            )
            db.commit()
        return True
    except Exception as e:
        print("UPDATE USER FIELDS FAIL : Error : ", e)
        return False

def check_fields_step1(data, fields=STEP1_FIELDS, profile_exists_check=True):
    result = {
        'success': True,
        'errors': []
    }
    for field in fields:
        if field not in data:
            result['success'] = False
            result['errors'].append(f"Field {field} is missing")
        else:
            if field == "username":
                if not isinstance(data[field], str):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not a string")
                else:
                    if len(data[field]) < 3:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too short")
                    if len(data[field]) > 255:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too long")
                    if not re.match(current_app.config['CONSTRAINTS']['username'], data[field]):
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid")
                    if profile_exists_check == True:
                        with get_db().cursor() as cur:
                            cur.execute('SELECT * FROM users WHERE username = %s', (data[field],))
                            user = cur.fetchone()
                            if user is not None:
                                result['success'] = False
                                result['errors'].append(f"Field {field} is already used")
            if field == "firstname" or field == "lastname":
                regex_name = current_app.config['CONSTRAINTS'][field]
                if not isinstance(data[field], str) or not re.match(regex_name, data[field]):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                else:
                    if len(data[field]) < 2:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too short")
                    if len(data[field]) > 32:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too long")
            if field == "age":
                if not isinstance(data[field], int):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not an int")
                else:
                    if data[field] < 15:
                        result['success'] = False
                        result['errors'].append(f"You must be at least 15 years old")
                    if data[field] > 80:
                        result['success'] = False
                        result['errors'].append(f"You are too old for this app")
            if field == "email":
                if not isinstance(data[field], str):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not a string")
                else:
                    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    if not re.match(email_regex, data[field]):
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid")
                    if profile_exists_check == True:
                        with get_db().cursor() as cur:
                            cur.execute('SELECT * FROM users WHERE email = %s', (data[field],))
                            user = cur.fetchone()
                            if user is not None:
                                result['success'] = False
                                result['errors'].append(f"Field {field} is already used")
            if field == "hetero":
                if not isinstance(data[field], bool) or data[field] not in [True, False]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "password":
                PASSWORD_ALLOWED_CHARACTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                SPECIAL_CHARACTERS = set("-/!@#$%^&*()_+;:,.?<>~`'\"{}[]|\\")
                
                password = data.get(field)
                
                if not isinstance(password, str):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not a string")
                else:
                    if len(password) < 8:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too short")
                    elif len(password) > 255:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too long")
                    else:
                        invalid_chars = [c for c in password if c not in PASSWORD_ALLOWED_CHARACTERS and c not in SPECIAL_CHARACTERS]
                        if invalid_chars:
                            result['success'] = False
                            result['errors'].append(f"Field {field} contains invalid characters: {', '.join(invalid_chars)}")
                        else:
                            has_lower = any(c.islower() for c in password)
                            has_upper = any(c.isupper() for c in password)
                            has_digit = any(c.isdigit() for c in password)
                            has_special = any(c in SPECIAL_CHARACTERS for c in password)

                            if not has_lower:
                                result['success'] = False
                                result['errors'].append("Password : at least one lowercase letter is required")
                            if not has_upper:
                                result['success'] = False
                                result['errors'].append("Password : at least one uppercase letter is required")
                            if not has_digit:
                                result['success'] = False
                                result['errors'].append("Password : at least one digit is required")
                            if not has_special:
                                result['success'] = False
                                result['errors'].append("Password : at least one special character is required")
                            if check_common_password(password):
                                result['success'] = False
                                result['errors'].append(f"Field {field} is too common")
            if field == "gender":
                if not isinstance(data[field], str) or data[field] not in ["M", "F"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
    return result

def check_common_password(password=""):
    password = password.lower()
    common_passwords = current_app.config['COMMON_PASSWORDS']
    for common_password in common_passwords:

        if common_password in password:
            print("Common password found", common_password, password)
            return True
    return False

def check_fields_step2(data, fields=STEP2_FIELDS):
    result = {
        'success': True,
        'errors': []
    }
    for field in fields:
        if field not in data:
            result['success'] = False
            result['errors'].append(f"Field {field} is missing")
        else:
            if field == "city":
                if not isinstance(data[field], str):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not a string")
                else:
                    city_id = get_city_id(data[field])
                    if city_id is None:
                        result['success'] = False
                        result['errors'].append(f"City {data[field]} not found")
            elif field == "searching":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['searching']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "commitment":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['commitment']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "frequency":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['frequency']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "weight":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['weight']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "size":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['size']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "shape":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['shape']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "smoking":
                if not isinstance(data[field], bool) or data[field] not in [True, False]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "alcohol":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['alcohol']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            elif field == "diet":
                if not isinstance(data[field], str) or data[field] not in current_app.config['CONSTRAINTS']['diet']:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
    return result

def check_fields_step3(data, fields=STEP3_FIELDS):
    result = {
        'success': True,
        'errors': []
    }
    for field in fields:
        if field not in data:
            result['success'] = False
            result['errors'].append(f"Field {field} is missing")
        else:
            if field == "interests":
                if not isinstance(data[field], list):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not a list")
                else:
                    if len(data[field]) < 4:
                        result['success'] = False
                        result['errors'].append(f"Field interests is not valid, at least 4 interests are required")
                    if len(data[field]) > 6:
                        result['success'] = False
                        result['errors'].append(f"Field interests is not valid, at most 6 interests are required")
                    seen = set()
                    for interest in data[field]:
                        if interest in seen:
                            result['success'] = False
                            result['errors'].append(f"Field {field}/{interest} is duplicated")
                        elif interest not in current_app.config['AVAILABLE_INTERESTS']:
                            result['success'] = False
                            result['errors'].append(f"Field {field}/{interest} is not valid")
                        else:
                            seen.add(interest)
            if field == "description":
                if not isinstance(data[field], str):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not a string")
                else:
                    if len(data[field]) < 10:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too short")
                    if len(data[field]) > 1500:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is too long")
                    if re.match(current_app.config["CONSTRAINTS"]["description"], data[field]) is None:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid")
    return result

def check_registration_status(other_email=None):
    if other_email is not None:
        user_email = other_email
    else:
        from flask_jwt_extended import verify_jwt_in_request
        try:
            verify_jwt_in_request()
            user_email = get_jwt_identity()
        except Exception as e:
            print("CHECK REGISTRATION STATIUS FAIL : No token provided : ", e)
            return False
    if user_email is None:
        return False
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (user_email,))
            user = cur.fetchone()
            if user is None:
                return False
            if user['registration_complete'] == True:
                return True
            else:
                for key, value in user.items():
                    if key == 'city_id' or key == 'email_token' or key == 'reset_token' or key == 'expiration':
                        continue
                    if value is None:
                        return False
                cur.execute('SELECT * FROM users_interests WHERE user_id = %s', (user['id'],))
                user_interests = cur.fetchone()
                if user_interests is None:
                    return False
                for key, value in user_interests.items():
                    if value is None:
                        return False
                cur.execute('UPDATE users SET registration_complete = TRUE WHERE email = %s', (user_email,))
                db.commit()
                return True
    except Exception as e:
        print("CHECK REGISTRATION STATIUS FAIL : Error : ", e)
        return False
    

def send_confirmation_email(email):
    mail_token = generate_email_token(email, "confirm")
    try:
        mail = current_app.config.get('MAIL', None)
        if mail:
            from flask_mail import Message
            msg = Message("Matcha - confirm email", sender=current_app.config["MAIL_USERNAME"], recipients=[email])
            from dotenv import load_dotenv
            load_dotenv()
            import os
            hostname = os.getenv('NGINX_HOST', None)
            if hostname is None:
                hostname = "localhost"
            if hostname == "localhost":
                hostname = "localhost:4200"
            else:
                hostname = hostname + ":8000"
            msg.body = f"Click on the following link to confirm your email : http://{hostname}/emailconfirm/" + mail_token
            mail.send(msg)
            return True
        else:
            print("Mail not configured")
            return True
    except Exception as e:
        print("SEND CONFIRMATION EMAIL FAIL : Failed to send email : Error : ", e)
        return False

def send_reset_password_email(email):
    mail_token = generate_email_token(email, system="reset")
    try:
        mail = current_app.config.get('MAIL', None)
        if mail:
            from flask_mail import Message
            msg = Message("Matcha - reset password", sender=current_app.config["MAIL_USERNAME"], recipients=[email])
            from dotenv import load_dotenv
            load_dotenv()
            import os
            hostname = os.getenv('NGINX_HOST', None)
            if hostname is None:
                hostname = "localhost"
            if hostname == "localhost":
                hostname = "localhost:4200"
            else:
                hostname = hostname + ":8000"
            msg.body = f"Click on the following link to reset your password : http://{hostname}/forgotpass/" + mail_token
            mail.send(msg)
            return True
        else:
            print("Mail not configured")
            return True
    except Exception as e:
        print("SEND RESET PASSWORD EMAIL FAIL : Failed to send email : Error : ", e)
        return False