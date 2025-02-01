from .db import get_db
import re
ALLOWED_CHARACTERS_BASE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"

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

def update_user_fields(user_informations, user_email):
    fields_updatable = ["firstname", "lastname", "email", "password", "age", "gender", "city", "searching", "commitment", "frequency", "weight", "size", "shape", "smoking", "alcohol", "diet", "description"]
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
                if not isinstance(data[field], dict):
                    result['success'] = False
                    result['errors'].append(f"Field {field} is not valid")
                else:
                    if "lon" not in data[field] or "lat" not in data[field]:
                        result['success'] = False
                        result['errors'].append(f"Field {field} is not valid")
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
            