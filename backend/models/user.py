from crypting import crypt_password, check_password
from database import createElem, getElems, modifyElem
from flask import session

from config import *

class User:
    table_name = 'users'
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'firstName': 'VARCHAR(30) NOT NULL',
        'lastName': 'VARCHAR(30) NOT NULL',
        'sexe': 'VARCHAR(1) NOT NULL',
        'CONSTRAINT check_sexe': "CHECK (sexe IN ('" + "', '".join(LIST_SEXE) + "'))",
        'age': 'INTEGER NOT NULL',
        'CONSTRAINT check_age': f"CHECK (age > {MIN_AGE} AND age < {MAX_AGE})",
        'email': 'VARCHAR(256) UNIQUE NOT NULL',
        'password': 'VARCHAR(256) NOT NULL',
        'description': 'VARCHAR(500) DEFAULT NULL',
        # categorie corps
        'poids': 'INTEGER DEFAULT NULL',
        'CONSTRAINT check_poids': f'CHECK (poids > {MIN_POIDS} AND poids < {MAX_POIDS})',
        'taille': 'INTEGER DEFAULT NULL',
        'CONSTRAINT check_taille': f'CHECK (taille > {MIN_TAILLE} AND taille < {MAX_TAILLE})',
        'corpulence': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_corpulance': f"CHECK (corpulence IN ('" + "', '".join(LIST_CORPU) + "'))",
        # categorie sante
        'fumeur': 'BOOLEAN DEFAULT NULL',
        'boit': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_boit': f"CHECK (boit IN ('" + "', '".join(LIST_BOIT) + "'))",
        'alimentation': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_alimentation': f"CHECK (alimentation IN ('" + "', '".join(LIST_ALIM) + "'))",
        # categorie relation ideale
        'recherche': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_recherche': "CHECK (recherche IN ('" + "', '".join(LIST_RECHERCHE) + "'))",
        'engagement': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_engagement': "CHECK (engagement IN ('" + "', '".join(LIST_ENGAGEMENT) + "'))",
        'frequence': 'VARCHAR(30) DEFAULT NULL',
        'CONSTRAINT check_frequence': "CHECK (frequence IN ('" + "', '".join(LIST_FREQUENCE) + "'))",
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
    if age < MIN_AGE or age > MAX_AGE:
        raise Exception('Age is not valid')
    sexe = user['sexe']
    if sexe not in LIST_SEXE:
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

def checkSanity(sanity, userId):
    if sanity['fumeur'] not in [True, False]:
        raise Exception('Invalid fumeur')
    if sanity['boit'] not in LIST_BOIT:
        raise Exception('Invalid boit')
    if sanity['alimentation'] not in LIST_ALIM:
        raise Exception('Invalid alimentation')
    modifyElem(User, userId, sanity)

def modifyUserBody(bodyInfo, userId):
    poids = bodyInfo['poids']
    if type(poids).__name__ != 'int':
        raise Exception('Invalid poids')
    taille = bodyInfo['taille']
    if type(taille).__name__ != 'int':
        raise Exception('Invalid taille')
    if poids < MIN_POIDS or poids > MAX_POIDS:
        raise Exception('Invalid poids')
    if taille < MIN_TAILLE or taille > MAX_TAILLE:
        raise Exception('Invalid taille')
    if bodyInfo['corpulence'] not in LIST_CORPU:
        raise Exception('Invalid corpulence')
    print(bodyInfo)
    modifyElem(User, userId, bodyInfo)

def modifyUserPersonnalInfo(personnalInfo, userId):
    Errors = []
    validUser = {}
    if 'firstName' in personnalInfo:
        firstName = personnalInfo['firstName']
        if firstName is not None:
            if checkInvalidCharacters(personnalInfo['firstName']) == True:
                Errors.append('Invalid characters in firstName')
            else:
                validUser['firstName'] = personnalInfo['firstName']
    if 'lastName' in personnalInfo:
        lastName = personnalInfo['lastName']
        if lastName is not None:
            if checkInvalidCharacters(personnalInfo['lastName']) == True:
                Errors.append('Invalid characters in lastName')
            else:
                validUser['lastName'] = personnalInfo['lastName']
    if 'email' in personnalInfo:
        email = personnalInfo['email']
        if email is not None:
            if emailValidator(personnalInfo['email'], doublonCheck=True) == False:
                Errors.append('Invalid email')
            else:
                validUser['email'] = personnalInfo['email']
    if 'age' in personnalInfo:
        age = personnalInfo['age']
        if age is not None:
            if type(age).__name__ != 'int':
                Errors.append('Invalid age')
            else:
                if age < MIN_AGE or age > MAX_AGE:
                    Errors.append('Invalid age')
                else:
                    validUser['age'] = personnalInfo['age']
    if 'sexe' in personnalInfo:
        sexe = personnalInfo['sexe']
        if sexe is not None:
            if sexe not in LIST_SEXE:
                Errors.append("Sexe is not valid")
            else:
                validUser['sexe'] = personnalInfo['sexe']
    if 'newPassword' in personnalInfo:
        newPassword = personnalInfo['newPassword']
        if newPassword is not None:
            if passwordValidator(newPassword) == False or newPassword != personnalInfo['newPasswordConfirm']:
                Errors.append('Password is not valid')
            else:
                validUser['password'] = crypt_password(newPassword)
    if len(Errors) > 0:
        strErrors = ', '.join(Errors)
        raise Exception(strErrors)
    if len(validUser) <= 0:
        raise Exception('No valid fields to modify')
    else:
        password = personnalInfo.get('password', None)
        if password is not None:
            user = getElems(User, {'id': userId})[0]
            if check_password(password, user[USER_ENUM['password']]) == True:
                print('password is correct')
                modifyElem(User, userId, validUser)
                session['email'] = validUser.get('email', session.get('email'))
            else:
                raise Exception('Invalid password')
        else:
            raise Exception('No password provided for modification')

def getPublicProfile(profileId):
    from .interests import getAllUsersInterest
    user = getElems(User, {'id': profileId})[0]
    userInterests = getAllUsersInterest(user[USER_ENUM['email']])
    return {
        'firstName': user[USER_ENUM['firstName']],
        'lastName': user[USER_ENUM['lastName']],
        'email': user[USER_ENUM['email']],
        'description': user[USER_ENUM['description']],
        'sexe': user[USER_ENUM['sexe']],
        'age': user[USER_ENUM['age']],
        'poids': user[USER_ENUM['poids']],
        'taille': user[USER_ENUM['taille']],
        'corpulence': user[USER_ENUM['corpulence']],
        'fumeur': user[USER_ENUM['fumeur']],
        'boit': user[USER_ENUM['boit']],
        'alimentation': user[USER_ENUM['alimentation']],
        'recherche': user[USER_ENUM['recherche']],
        'engagement': user[USER_ENUM['engagement']],
        'frequence': user[USER_ENUM['frequence']],
        'interests': userInterests
    }
