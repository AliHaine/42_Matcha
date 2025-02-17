from .db import get_db
from .cities import get_city_id
import re
from flask_jwt_extended import jwt_required, get_jwt_identity
ALLOWED_CHARACTERS_BASE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"
from flask import current_app

def create_user(user_informations):
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                'INSERT INTO users (firstname, lastname, email, password, age, gender) VALUES (%s, %s, %s, %s, %s, %s)',
                (user_informations['firstname'], user_informations['lastname'], user_informations['email'], user_informations['password'], user_informations['age'], user_informations['gender'])
            )
        db.commit()
        return True
    except Exception as e:
        print("Failed to create user (func : create_user, file : user.py). Error : ", e)
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
        print("Failed to update interests (func : update_interests, file : user.py). Error : ", e)
        return False

def update_user_fields(user_informations, user_email):
    fields_updatable = ["firstname", "lastname", "email", "password", "age", "gender", "city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet", "description", "interests", "hetero"]
    if not isinstance(user_informations, dict):
        return False
    if not isinstance(user_email, str):
        return False
    if len(user_email) == 0:
        return False
    try:
        values = []
        for key, value in user_informations.items():
            if key in fields_updatable:
                values.append(value)
            else:
                raise Exception(f"Invalid field {key}")
        db = get_db()
        with db.cursor() as cur:
            values_name = ""
            values_content = tuple()
            for key, value in user_informations.items():
                if key in fields_updatable:
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
        print("Failed to update user fields (func : update_user_fields, file : user.py). Error : ", e)
        return False

def check_fields_step1(data, fields=["firstname", "lastname", "email", "password", "age", "gender"], email_exists_check=True):
    result = {
        'success': True,
        'errors': []
    }
    for field in fields:
        if field not in data:
            result['success'] = False
            result['errors'].append(f"Field {field} is missing")
        else:
            if field == "firstname" or field == "lastname":
                if not isinstance(data[field], str) or not all(c in ALLOWED_CHARACTERS_BASE + " " for c in data[field]):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                if len(data[field]) < 2 or len(data[field]) > 20:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "age":
                if not isinstance(data[field], int) or data[field] < 15 or data[field] > 80:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "email":
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not isinstance(data[field], str) or not re.match(email_regex, data[field]):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                if email_exists_check == True:
                    with get_db().cursor() as cur:
                        cur.execute('SELECT * FROM users WHERE email = %s', (data[field],))
                        user = cur.fetchone()
                        if user is not None:
                            result['success'] = False
                            result['errors'].append(f"Field {field} is already used")
            if field == "password":
                PASSWORD_ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/!@#$%^&*()_+"
                if not isinstance(data[field], str) or len(data[field]) < 8:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                lower = 0
                upper = 0
                digit = 0
                special = 0
                for c in data[field]:
                    if c not in PASSWORD_ALLOWED_CHARACTERS:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid")
                        break
                    if c.islower():
                        lower += 1
                    if c.isupper():
                        upper += 1
                    if c.isdigit():
                        digit += 1
                    if c in "/!@#$%^&*()_+":
                        special += 1
                if lower == 0 or upper == 0 or digit == 0 or special == 0:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "gender":
                if not isinstance(data[field], str) or data[field] not in ["M", "F"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
    return result

def check_fields_step2(data, fields=["city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet"]):
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
                pass
#                 if not isinstance(data[field], dict):
#                     result['success'] = False
#                     result['errors'].append(f"Field {field} is not valid")
#                 else:
#                     if "lon" not in data[field] or "lat" not in data[field]:
#                         result['success'] = False
#                         result['errors'].append(f"Field {field} is not valid")
#                     else:
#                         if isinstance(data[field]["lon"], float) == False or isinstance(data[field]["lat"], float) == False:
#                             result['success'] = False
#                             result['errors'].append(f"Field {field} is not valid")
            elif field == "hetero":
                if not isinstance(data[field], bool) or data[field] not in [True, False]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
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

def check_fields_step3(data, fields=["interests", "description"]):
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
                    result['errors'].append(f"Field {field} is not valid")
                else:
                    if len(data[field]) == 0:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid (not enough interests)")
                    for interest in data[field]:
                        if interest not in current_app.config['AVAILABLE_INTERESTS']:
                            result['success'] = False
                            result['errors'].append(f"Field {field}/{interest} is not valid")
            if field == "description":
                if not isinstance(data[field], str) or len(data[field]) < 10 or len(data[field]) > 1500:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
    return result

@jwt_required()
def check_registration_status(other_email=None):
    if other_email is not None:
        user_email = other_email
    else:
        user_email = get_jwt_identity()
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
                    if key == 'city_id':
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
        print("Failed to check registration status (func : check_registration_status, file : user.py). Error : ", e)
        return False