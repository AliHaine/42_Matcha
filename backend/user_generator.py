import sys
from random import sample, choice
import requests
import psycopg2

connection = psycopg2.connect(database="matcha", user="admin", password="admin/0123456789", host="localhost", port=6000)
cursor = connection.cursor()

link = "https://randomuser.me/api/?nat=fr"


interests = requests.get("http://localhost:8000/api/getInterests").json()['interests']
print(f"interests setup: {interests}")
def get_interests(number):
    return sample(interests, number)


commitment = requests.get("http://localhost:8000/api/getIdealRelation").json()
print(f"commitment setup: {commitment}")
def get_commitment(data_to_send):
    data_to_send["engagement"] = choice(commitment['engagement'])
    data_to_send["frequency"] = choice(commitment['frequency'])
    data_to_send["research"] = choice(commitment['research'])


def get_user():
    request = requests.get(link)
    result = request.json()['results']
    print(result)
    return result


def get_data_to_send(result):
    data_to_send = {}
    data_to_send['firstname'] = result[0]['name']['first']
    data_to_send['lastname'] = result[0]['name']['last']
    data_to_send['age'] = result[0]['dob']['age']
    data_to_send['sex'] = result[0]['gender'][0].upper()
    data_to_send['email']= f"{data_to_send['firstname']}.{data_to_send['lastname']}.{data_to_send['age']}@gmail.com"
    data_to_send['password'] = "Pamda666!"
    data_to_send['description'] = "default descritiopn"
    get_commitment(data_to_send)
    return data_to_send


def execute_sql(data_to_send):
    cursor.execute("""
        INSERT INTO users (firstname, lastname, sex, age, email, password, description, weight, height, corpu, smoking, drink, diet, research, engagement, frequency) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        data_to_send['firstname'],
        data_to_send['lastname'],
        data_to_send['sex'],
        data_to_send['age'],
        data_to_send['email'],
        data_to_send['password'],
        data_to_send['description'],
        50,  # You can keep this as a static value or pass it dynamically too
        150,  # Same for this one
        'normal',
        False,  # Boolean value for smoking
        'never',  # Static string value for drink
        'omnivore',  # Static value for diet
        data_to_send['research'],
        data_to_send['engagement'],
        data_to_send['frequency']
    ))
    connection.commit()

for i in range(int(sys.argv[1])):
    user_response = get_user()
    data_to_send = get_data_to_send(user_response)
    execute_sql(data_to_send)
    print("New user created")