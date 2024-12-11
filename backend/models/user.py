from crypting import crypt_password, check_password
from database import createElem, getElems
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- "
PASSWORD_REQUIREMENTS = {
    'min_length': 8,
    'min_uppercase': 1,
    'min_lowercase': 1,
    'min_digits': 1
}


class User:
    table_name = 'users'
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'firstName': 'VARCHAR(100)',
        'email': 'VARCHAR(100) UNIQUE',
        'password': 'VARCHAR(100)',
        'description': 'VARCHAR(500)'
    }
# interets a rajouter (voir chatgpt outlook, chat colonnes liste dans bdd)
# se renseigner pour les photos de profil
# se renseigner sur les villes (api du gouvernement)

def checkInvalidCharacters(string: str) -> bool:
    invalidCharacters = ALLOED_CHARACTERS
    for character in invalidCharacters:
        if character in string:
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
    if checkInvalidCharacters(user['firstName']) or checkInvalidCharacters(user['lastName']):
        raise Exception('Invalid characters in user data')
    if emailValidator(user['email']) == False:
        raise Exception('Invalid characters in email')
    password = user['password']
    if passwordValidator(password) == False:
        raise Exception('Password is not valid')
    if password != user['passwordConfirm']:
        raise Exception('Passwords do not match')
    user['password'] = crypt_password(user['password'])
    createElem(User, user)


def login_user_func(request, userToLogin):
    email = userToLogin['email']
    password = userToLogin['password']
    if emailValidator(email, doublonCheck=False) == False:
        raise Exception('Invalid characters in email')
    users = getElems(User, {'email': email})
    if len(users) == 0:
        raise Exception('User not found')
    user = users[0]
    print(user)
    if check_password(password, user[4]) == True:
        pass
    else:
        raise Exception('Invalid password')