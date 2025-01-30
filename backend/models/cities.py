from database import getElems, createElem
import requests

class UserCity:
    table_name = 'user_city'
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'user_id': 'INT NOT NULL',
        'city_id': 'INT NOT NULL',
        'FOREIGN KEY (user_id)': 'REFERENCES users(id) ON DELETE CASCADE',
        'FOREIGN KEY (city_id)': 'REFERENCES cities(id) ON DELETE CASCADE',
    }

class cities:
    table_name = 'cities'
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'cityname': 'VARCHAR(250) NOT NULL',
        'citycode': 'INT NOT NULL',
        'departementname': 'VARCHAR(250) NOT NULL',
        'departementcode': 'INT NOT NULL',
        'regionname': 'VARCHAR(250)',
        'regioncode': 'INT',
    }

def checkCity(city):
    res = getElems(cities, {'cityname': city['nom']})
    if len(res) == 0:
        print(f'City {city} not found in database, adding it')
        cityCreation = {
            'cityname': city['nom'],
            'citycode': city['code'],
            'departementname': city['departement']['nom'],
            'departementcode': city['departement']['code'],
            'regionname': city['region']['nom'],
            'regioncode': city['region']['code'],
        }
        createElem(cities, cityCreation)
    else:
        print(f'City {city} found in database')
    cityID = getElems(cities, {'cityname': city['nom']})[0][0]
    return cityID