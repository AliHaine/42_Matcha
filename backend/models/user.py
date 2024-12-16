from crypting import crypt_password, check_password
from database import createElem, getElems
from flask import session

ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- "
PASSWORD_REQUIREMENTS = {
    'min_length': 8,
    'min_uppercase': 1,
    'min_lowercase': 1,
    'min_digits': 1
}
REQUIRED_FIELDS = ['firstName', 'lastName', 'email', 'password', 'sexe', 'age']

USER_ENUM = {
    'id': 0,
    'firstName': 1,
    'lastName': 2,
    'sexe': 3,
    'age': 4,
    'email': 5,
    'password': 6,
    'description': 7
}
class User:
    table_name = 'users'
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'firstName': 'VARCHAR(30) NOT NULL',
        'lastName': 'VARCHAR(30) NOT NULL',
        'sexe': 'VARCHAR(1) NOT NULL',
        'CONSTRAINT check_sexe': 'CHECK (sexe IN (\'H\', \'F\'))',
        'age': 'INTEGER NOT NULL',
        'email': 'VARCHAR(256) UNIQUE NOT NULL',
        'password': 'VARCHAR(256) NOT NULL',
        'description': 'VARCHAR(500) DEFAULT NULL',
        # categorie corps
        'poids': 'INTEGER DEFAULT NULL',
        'taille': 'INTEGER DEFAULT NULL',
        'corpulance': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_corpulance': 'CHECK (corpulance IN (\'mince\', \'normal\', \'sportif\', \'fort\'))',
        # categorie sante
        'fumeur': 'BOOLEAN DEFAULT NULL',
        'Boit': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_boit': 'CHECK (Boit IN (\'jamais\', \'occasionnel\', \'souvent\'))',
        'alimentation': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_alimentation': 'CHECK (alimentation IN (\'vegetarien\', \'vegan\', \'carnivore\', \'omnivore\'))',
        # categorie relation ideale
        'recherche': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_recherche': 'CHECK (recherche IN (\'amicale\', \'amoureuse\', \'sexuelle\', \'aucune idee\', \'discussion uniquement\'))',
        'engagement': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_engagement': 'CHECK (engagement IN (\'court terme\', \'long terme\', \'aucune idee\'))',
        'frequence': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_frequence': 'CHECK (frequence IN (\'Quotidienne\', \'Hebdomadaire\', \'Occassionnelle\', \'autre\'))',

    }

# TODO
# interets a rajouter (voir chatgpt outlook, chat colonnes liste dans bdd)
# se renseigner pour les photos de profil
# se renseigner sur les villes (api du gouvernement)

def checkInvalidCharacters(string: str) -> bool:
    allowedCharacters = ALLOWED_CHARACTERS
    for character in string:
        if character not in allowedCharacters:
            return True    
    return False

def passwordValidator(password: str) -> bool:
    if len(password) < PASSWORD_REQUIREMENTS['min_length']:
        return False
    if sum([1 for character in password if character.isupper()]) < PASSWORD_REQUIREMENTS['min_uppercase']:
        return False
    if sum([1 for character in password if character.islower()]) < PASSWORD_REQUIREMENTS['min_lowercase']:
        return False
    if sum([1 for character in password if character.isdigit()]) < PASSWORD_REQUIREMENTS['min_digits']:
        return False
    return True

def emailValidator(email: str, doublonCheck=True) -> bool:
    if '@' not in email:
        return False
    if '.' not in email:
        return False
    tab = email.split('@')
    if len(tab) != 2:
        return False
    if tab[0] == '' or tab[1] == '':
        return False
    tab = tab[1].split('.')
    if len(tab) != 2:
        return False
    if tab[0] == '' or tab[1] == '':
        return False
    if doublonCheck == True:
        emails = getElems(User, {'email': email})
        if len(emails) > 0:
            raise Exception('Email already exists')
    return True

def create_user(user):
    if checkInvalidCharacters(user['firstName']) == True or checkInvalidCharacters(user['lastName']) == True:
        raise Exception('Invalid characters in name')
    if emailValidator(user['email']) == False:
        raise Exception('Invalid email')
    password = user['password']
    if passwordValidator(password) == False:
        raise Exception('Password is not valid')
    if password != user['passwordConfirm']:
        raise Exception('Passwords do not match')
    age = user['age']
    if age <= 15 or age > 80:
        raise Exception('Age is not valid')
    sexe = user['sexe']
    if sexe != 'H' and sexe != 'F':
        raise Exception("Sexe is not valid")
    user['password'] = crypt_password(user['password'])
    createElem(User, user, REQUIRED_FIELDS)
    user['password'] = password


def login_user_func(userToLogin):
    email = userToLogin.get('email', '')
    password = userToLogin.get('password', '')
    if emailValidator(email, doublonCheck=False) == False:
        raise Exception('Invalid email')
    users = getElems(User, {'email': email})
    if len(users) == 0:
        raise Exception('User not found')
    user = users[0]
    if check_password(password, user[USER_ENUM['password']]) == True:
        session['email'] = email
    else:
        raise Exception('Invalid password')