from database import getElems
import requests

class UserCity:
    table_name = 'user_city'
    columns = {
        'user_id': 'INT NOT NULL',
        'city_id': 'INT NOT NULL',
        'PRIMARY KEY (user_id, city_id)': '',
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
    }

# def checkIfCityExistsInDB(cityName):
#     cities = getElems(cities, details={'cityname': cityName})
#     if len(cities) > 0:
#         return cities[0]
#     return None

# def addNewCity(cityName, cityCode, departementName, departementCode):
#     res = requests.get(f'https://api-adresse.data.gouv.fr/search/?q={cityName}&limit=1')