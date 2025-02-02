from .db import get_db
import requests

def get_city_id(coordinates):
    city_informations = requests.get(f"https://geo.api.gouv.fr/communes?lat={coordinates['lat']}&lon={coordinates['lon']}&fields=code,nom,departement,region,centre").json()

    if len(city_informations) == 0:
        return None
    print(city_informations)
    city_informations = city_informations[0]
    db = get_db()
    with db.cursor() as cur:
        print("\n\n\n\ntest region BEFORE")
        cur.execute('SELECT * FROM cities WHERE cityname = %s', (city_informations["nom"],))
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO cities (cityname, citycode, departementname, departementcode, regionname, regioncode, centerlon, centerlat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (city_informations["nom"], city_informations["code"], city_informations["departement"]["nom"], city_informations["departement"]["code"], city_informations["region"]["nom"], city_informations["region"]["code"], city_informations["centre"]["coordinates"][0], city_informations["centre"]["coordinates"][1],))
            db.commit()
            cur.execute('SELECT * FROM cities WHERE cityname = %s', (city_informations["nom"],))
            result = cur.fetchone()
        print("\n\n\n\ntest region AFTER", result)
        return result['id']
    return None