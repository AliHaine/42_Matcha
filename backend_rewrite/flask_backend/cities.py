from .db import get_db
import requests

def get_city_id(cityname):
    citycode = cityname.split(" ")[-1]
    citycode = citycode[1:len(citycode) - 1]
    cityname = cityname[0:(len(cityname) - len(citycode) - 2)].strip()
    city_informations = requests.get(f"https://geo.api.gouv.fr/communes?boost=population&limit=5&nom={cityname}&codePostal={citycode}&fields=nom,departement,region,centre,codesPostaux").json()
    if len(city_informations) == 0:
        return None
    city_found = False
    for city in city_informations:
        if city["nom"].lower() == cityname.lower():
            city_informations = city
            city_found = True
            break
    if not city_found:
        return None
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT * FROM cities WHERE cityname = %s', (city_informations["nom"],))
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO cities (cityname, citycode, departementname, departementcode, regionname, regioncode, centerlon, centerlat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (city_informations["nom"], city_informations["codesPostaux"][0], city_informations["departement"]["nom"], city_informations["departement"]["code"], city_informations["region"]["nom"], city_informations["region"]["code"], city_informations["centre"]["coordinates"][0], city_informations["centre"]["coordinates"][1],))
            db.commit()
            cur.execute('SELECT * FROM cities WHERE cityname = %s', (city_informations["nom"],))
            result = cur.fetchone()
        return result['id']
    return None