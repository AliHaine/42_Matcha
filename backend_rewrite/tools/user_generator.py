import sys
from random import sample, choice, random
import requests
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
import re

connection = psycopg2.connect(database="matcha", user="admin", password="admin/0123456789", host="localhost", port=6000)
cursor = connection.cursor()

link = "https://randomuser.me/api/?nat=fr&inc=name,dob,gender&results="

def populate_cities():
    city_link = "https://geo.api.gouv.fr/communes?limit=1000&fields=nom,code,departement,region,centre"
    city_data = requests.get(city_link).json()
    if not city_data:
        print("Aucune donnée de ville disponible.")
        return

    query = """
    INSERT INTO cities (cityname, citycode, departementname, departementcode, regionname, regioncode, centerlon, centerlat) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    data_list = []
    for city in city_data:
        try:
            lon, lat = city["centre"]["coordinates"]
            data_list.append((
                city["nom"], 
                city["code"],
                city["departement"]["nom"],
                city["departement"]["code"],
                city["region"]["nom"],
                city["region"]["code"],
                city["centre"]["coordinates"][0],
                city["centre"]["coordinates"][1],
            ))
        except KeyError:
            print(f"⚠ Données manquantes pour {city}")

    if data_list:
        cursor.executemany(query, data_list)
        connection.commit()
        print(f"{len(data_list)} villes insérées dans la base de données.")
    else:
        print("Aucune ville à insérer.")


weight_choices = ['-50', '51-60', '61-70', '71-80', '81-90', '91-100', '+100']
size_choices = ['-150', '151-160', '161-170', '171-180', '181-190', '191-200', '+200']
shape_choices = ['Skinny', 'Normal', 'Sporty', 'Fat']
smoking_choices = [True, False]
alcohol_choices = ['Never', 'Occasionally', 'Every week', 'Every day']
diet_choices = ['Omnivor', 'Vegetarian', 'Vegan', 'Rich in protein']
searching_choices = ['Friends', 'Love', 'Talking']
commitment_choices = ['Short term', 'Long term', 'Undecided']
frequency_choices = ['Daily', 'Weekly', 'Occasionally']

def get_user(batch=1):
    request = requests.get(link + str(batch))
    result = request.json()['results']
    return result


from unidecode import unidecode
def get_data_to_send(result):
    return (
        result['name']['first'],
        result['name']['last'],
        unidecode(f"{result['name']['first']}.{result['name']['last']}{min_mail}@randomusers.py".lower().replace(" ", "")),
        generate_password_hash("Panda666!"),
        result['dob']['age'] % 12 + 18,
        result['gender'][0].upper(),
        choice(city_ids),
        choice(searching_choices),
        choice(commitment_choices),
        choice(frequency_choices),
        "default description",
        choice(weight_choices),
        choice(size_choices),
        choice(shape_choices),
        choice(smoking_choices),
        choice(alcohol_choices),
        choice(diet_choices),
        choice([True, False]),
        True,
        True,
    )


def insert_users(data):
    query = """
        INSERT INTO users (firstname, lastname, email, password, age, gender, city_id, searching, commitment, frequency, description, weight, size, shape, smoking, alcohol, diet, hetero, registration_complete, email_verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    cursor.executemany(query, data)
    connection.commit()

print("User generator started")
cursor.execute("SELECT COUNT(*) FROM cities")
if cursor.fetchone()[0] == 0:
    populate_cities()
cursor.execute("SELECT id FROM cities")
city_ids = cursor.fetchall()
city_ids = [city[0] for city in city_ids]
max_users = int(sys.argv[1])
cursor.execute("SELECT COUNT(*) FROM users")
min_mail = cursor.fetchone()[0]
if min_mail > 0:
    print(f"La base de données contient déjà {min_mail} utilisateurs.")
batch_size = 1000
try:
    while max_users > 0:
        if max_users > 5000:
            print(f"Fetching 5000 users")
            users = get_user(5000)
            max_users -= 5000
        else:
            print(f"Fetching {max_users} users")
            users = get_user(max_users)
            max_users = 0
        print(f"{len(users)} users fetched, starting conversion")
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]
            data = []
            for user in batch:
                min_mail += 1
                data.append(get_data_to_send(user))
            print("conversion done, starting insertion")
            insert_users(data)
            print(f"Insertion done, {len(batch)} users inserted in this batch.")
        
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()

