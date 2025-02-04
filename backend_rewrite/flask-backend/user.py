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
                print("adding interest", interest)
                cur.execute('SELECT id FROM interests WHERE name = %s', (interest,))
                interest_id = cur.fetchone()['id']
                cur.execute('INSERT INTO users_interests (user_id, interest_id) VALUES (%s, %s)', (user_id, interest_id))
        db.commit()
        return True
    except Exception as e:
        print("Failed to update interests (func : update_interests, file : user.py). Error : ", e)
        return False

def update_user_fields(user_informations, user_email):
    fields_updatable = ["firstname", "lastname", "email", "password", "age", "gender", "city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet", "description", "interests"]
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
                print("firstname or lastname")
                if not isinstance(data[field], str) or not all(c in ALLOWED_CHARACTERS_BASE + " " for c in data[field]):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                if len(data[field]) < 2 or len(data[field]) > 20:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "age":
                print("age", data[field])
                if not isinstance(data[field], int) or data[field] < 15 or data[field] > 80:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "email":
                print("email")
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
                print("password")
                if not isinstance(data[field], str) or len(data[field]) < 8 or not any(c.isupper() for c in data[field]) or not any(c.islower() for c in data[field]) or not any(c.isdigit() for c in data[field]):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "gender":
                print("gender")
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
                print("city")
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
            if field == "searching":
                print("searching")
                if not isinstance(data[field], str) or data[field] not in ["Friends", "Love", "Just talking"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "commitment":
                print("commitment")
                if not isinstance(data[field], str) or data[field] not in ["Short term", "Long term", "Undecided"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "frequency":
                print("frequency")
                if not isinstance(data[field], str) or data[field] not in ["Daily", "Weekly", "Occasionally"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "weight":
                print("weight")
                if not isinstance(data[field], str) or data[field] not in ["< 50", "51-60", "61-70", "71-80", "81-90", "91-100", "> 100"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "size":
                print("size")
                if not isinstance(data[field], str) or data[field] not in ["< 150", "151-160", "161-170", "171-180", "181-190", "191-200", "> 200"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "shape":
                print("shape")
                if not isinstance(data[field], str) or data[field] not in ["Skinny", "Normal", "Sporty", "Fat"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "smoking":
                print("smoking")
                if not isinstance(data[field], bool) or data[field] not in [True, False]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "alcohol":
                print("alcohol")
                if not isinstance(data[field], str) or data[field] not in ["Never", "Occasionally", "Every week", "Every day"]:
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
            if field == "diet":
                print("diet")
                if not isinstance(data[field], str) or data[field] not in ["Omnivor", "Vegetarian", "Vegan", "Rich in protein"]:
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
                print("interests")
                if not isinstance(data[field], list):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                else:
                    print(data[field])
                    if len(data[field]) == 0:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid (not enough interests)")
                    for interest in data[field]:
                        if interest not in current_app.config['AVAILABLE_INTERESTS']:
                            result['success'] = False
                            result['errors'].append(f"Field {field} is not valid")
            if field == "description":
                print("description")
                if not isinstance(data[field], str) or len(data[field]) < 10 or len(data[field]) > 500:
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
            print("checking this user registration status :", user)
            if user['registration_complete'] == True:
                return True
            else:
                for key, value in user.items():
                    if value is None:
                        return False
                cur.execute('SELECT * FROM users_interests WHERE user_id = %s', (user['id'],))
                user_interests = cur.fetchone()
                if user_interests is None:
                    return False
                for key, value in user_interests.items():
                    if key == 'city_id':
                        continue
                    if value is None:
                        return False
                cur.execute('UPDATE users SET registration_complete = TRUE WHERE email = %s', (user_email,))
                db.commit()
                return True
    except Exception as e:
        print("Failed to check registration status (func : check_registration_status, file : user.py). Error : ", e)
        return False