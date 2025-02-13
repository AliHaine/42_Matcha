import sys
from random import sample, choice
import requests
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash

connection = psycopg2.connect(database="matcha", user="admin", password="admin/0123456789", host="localhost", port=6000)
cursor = connection.cursor()

link = "https://randomuser.me/api/?nat=fr"


interests = requests.get("http://localhost:5000/api/getInformations/interests").json()['interests']["Other"]
def get_interests(number):
    return sample(interests, number)


commitment = {
    "searching": ["Friends", "Love", "Just talking"],
    "commitment": ["Short term", "Long term", "Undecided"],
    "frequency": ["Daily", "Weekly", "Occasionally"]
}
def get_commitment(data_to_send):
    data_to_send["searching"] = choice(commitment['searching'])
    data_to_send["commitment"] = choice(commitment['commitment'])
    data_to_send["frequency"] = choice(commitment['frequency'])


def get_user():
    request = requests.get(link)
    result = request.json()['results']
    return result


def get_data_to_send(result):
    data_to_send = {}
    data_to_send['firstname'] = result[0]['name']['first']
    data_to_send['lastname'] = result[0]['name']['last']
    data_to_send['age'] = result[0]['dob']['age']
    data_to_send['gender'] = result[0]['gender'][0].upper()
    data_to_send['email']= f"{data_to_send['firstname']}.{data_to_send['lastname']}.{data_to_send['age']}@gmail.com"
    data_to_send['password'] = generate_password_hash("Panda666!")
    data_to_send['description'] = "default descritiopn"
    get_commitment(data_to_send)
    return data_to_send

##city_id               | integer                     |           |          |
## created_at            | timestamp without time zone |           | not null | CURRENT_TIMESTAMP
## status                | character varying(255)      |           |          | 'Inactive'::character varying
## pictures_number       | integer                     |           |          | 0
## registration_complete | boolean                     |           |          | false

def execute_sql(data_to_send):
    cursor.execute("""
        INSERT INTO users (firstname, lastname, gender, age, email, password, description, weight, size, shape, smoking, alcohol, diet, searching, commitment, frequency, registration_complete) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        data_to_send['firstname'],
        data_to_send['lastname'],
        data_to_send['gender'],
        data_to_send['age'],
        data_to_send['email'],
        data_to_send['password'],
        data_to_send['description'],
        "91-100",
        "181-190",
        'Normal',
        False,  # Boolean value for smoking
        'Never',  # Static string value for drink
        'Omnivor',  # Static value for diet
        data_to_send['searching'],
        data_to_send['commitment'],
        data_to_send['frequency'],
        True
    ))
    connection.commit()

for i in range(int(sys.argv[1])):
    user_response = get_user()
    data_to_send = get_data_to_send(user_response)
    execute_sql(data_to_send)
