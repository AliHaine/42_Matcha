import sys
from random import sample, choice, random
import requests
import psycopg2
from tqdm import tqdm
from werkzeug.security import generate_password_hash
from concurrent.futures import ThreadPoolExecutor  # ou ProcessPoolExecutor

import os

max_workers = os.cpu_count() - 1

connection = psycopg2.connect(database="matcha", user="admin", password="admin/0123456789", host="localhost", port=6000)
cursor = connection.cursor()

link = "https://randomuser.me/api/?nat=fr&inc=name,dob,gender&results="

def populate_cities():
    city_link = "https://geo.api.gouv.fr/communes?limit=100000&fields=nom,code,departement,region,centre,population"
    response = requests.get(city_link)

    if response.status_code == 200:
        communes = response.json()
        communes = [c for c in communes if c.get("population") is not None]
        communes_sorted = sorted(communes, key=lambda x: x["population"], reverse=True)
        print(f"Récupération de {len(communes_sorted)} villes : {[c['nom'] for c in communes_sorted]}")

        city_data = communes_sorted[:100]
    else:
        print(f"Erreur lors de l'appel API : {response.status_code}")
    print(f"Récupération de {len(city_data)} villes : {[c['nom'] for c in city_data]}")
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
def get_data_to_send(args):
    user, user_id = args
    return (
        user['name']['first'],
        user['name']['last'],
        unidecode(f"{user['name']['first']}.{user['name']['last']}{user_id}@randomusers.py".lower().replace(" ", "")),
        generate_password_hash("Panda666!"),
        user['dob']['age'] % 50 + 15,
        user['gender'][0].upper(),
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
if cursor.fetchone()[0] < 10:
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
            print(f"conversion de {len(batch)} utilisateurs…")

            # Préparer les arguments avec leurs IDs
            batch_ids = list(range(user_id_start + 1, user_id_start + 1 + len(batch)))
            args = list(zip(batch, batch_ids))

            # Conversion parallèle
            with ThreadPoolExecutor(max_workers=max_workers) as executor:  # Ajuste selon ton CPU
                data = list(tqdm(executor.map(get_data_to_send, args), total=len(args), desc=f"🔄 Conversion batch"))
            # Mise à jour de l'ID de départ
            user_id_start += len(data)

            # Génération des intérêts
            interests = []
            for uid in range(user_id_start - len(data) + 1, user_id_start + 1):
                for _ in range(5):
                    interest_id = choice(range(1, possible_interests + 1))
                    while (uid, interest_id) in interests:
                        interest_id = choice(range(1, possible_interests + 1))
                    interests.append((uid, interest_id))

            print("conversion des données terminée, debut de l'insertion")
            insert_users(data)
            insert_interests(interests)
            print(f"Insertion de {len(data)} utilisateurs terminée, temps écoulé : {datetime.now() - start_time}")
except Exception as e:
    print(e, "Erreur lors de l'insertion des utilisateurs")
finally:
    cursor.close()
    connection.close()

print(f"Fin de la génération d'utilisateurs à : {datetime.now()}")
print(f"Temps écoulé : {datetime.now() - start_time}")
print(f"Nombre total d'utilisateurs insérés : {baseinput_users - remaining_users}")
print(f"Nombre total d'utilisateurs restants : {remaining_users}")
