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
from datetime import datetime
def get_data_to_send(result):
    return (
        result['name']['first'],
        result['name']['last'],
        unidecode(f"{result['name']['first']}.{result['name']['last']}{user_id_start}@randomusers.py".lower().replace(" ", "")),
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

def insert_interests(data):
    query = """
        INSERT INTO users_interests (user_id, interest_id)
        VALUES (%s, %s);
        """
    cursor.executemany(query, data)
    connection.commit()

cursor.execute("SELECT COUNT(*) FROM cities")
if cursor.fetchone()[0] == 0:
    populate_cities()
cursor.execute("SELECT id FROM cities")
city_ids = cursor.fetchall()
city_ids = [city[0] for city in city_ids]
remaining_users = int(sys.argv[1])
baseinput_users = remaining_users
cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
user_id_start = cursor.fetchone()
if user_id_start is None:
    user_id_start = 0
else:
    user_id_start = user_id_start[0]
if user_id_start > 0:
    print(f"La base de données contient déjà {user_id_start} utilisateurs.")
batch_size = 5000
start_time = datetime.now()
cursor.execute("SELECT COUNT(*) FROM interests")
possible_interests = cursor.fetchone()[0]
print(f"Debut de la génération d'utilisateurs à : {start_time}")
try:
    while remaining_users > 0:
        if remaining_users > 5000:
            print(f"recuperation de 5000 utilisateurs")
            users = get_user(5000)
            remaining_users -= 5000
        else:
            print(f"recuperation de {remaining_users} utilisateurs")
            users = get_user(remaining_users)
            remaining_users = 0
        print(f"{len(users)} utilisateurs récupérés, debut de la conversion des données")
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]
            data = []
            interests = []
            for user in batch:
                user_id_start += 1
                data.append(get_data_to_send(user))
                print(f"conversion de {len(data)}/{len(batch)} utilisateurs terminée", end="\r")
                for _ in range(5):
                    interest_id = choice(range(1, possible_interests + 1))
                    while (user_id_start, interest_id) in interests:
                        interest_id = choice(range(1, possible_interests + 1))
                    interests.append((user_id_start, interest_id))
            print("conversion des données terminée, debut de l'insertion")
            insert_users(data)
            insert_interests(interests)
            print(f"Insertion de {len(data)} utilisateurs terminée, {remaining_users + len(users) - len(batch)}/{baseinput_users} restants, temps écoulé : {datetime.now() - start_time}")
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()

print(f"Fin de la génération d'utilisateurs à : {datetime.now()}")
print(f"Temps écoulé : {datetime.now() - start_time}")
print(f"Nombre total d'utilisateurs insérés : {baseinput_users - remaining_users}")
print(f"Nombre total d'utilisateurs restants : {remaining_users}")
