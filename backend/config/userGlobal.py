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

LIST_SEXE = ['H', 'F']
MIN_AGE = 15
MAX_AGE = 80
MAX_POIDS = 300
MIN_POIDS = 30
MAX_TAILLE = 250
MIN_TAILLE = 90
LIST_CORPU = ['mince', 'normal', 'sportif', 'fort']
LIST_BOIT = ['jamais', 'occasionnel', 'souvent']
LIST_ALIM = ['vegetarien', 'vegan', 'carnivore', 'omnivore']
LIST_RECHERCHE = ['amicale', 'amoureuse', 'aucune idee']
LIST_ENGAGEMENT = ['court terme', 'long terme', 'aucune idee']
LIST_FREQUENCE = ['Quotidienne', 'Hebdomadaire', 'Occassionnelle', 'autre']