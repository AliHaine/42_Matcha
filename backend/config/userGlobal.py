# pour la creation d'un utilisateur
ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- "
PASSWORD_REQUIREMENTS = {
    'min_length': 8,
    'min_uppercase': 1,
    'min_lowercase': 1,
    'min_digits': 1
}
REQUIRED_FIELDS = ['firstName', 'lastName', 'email', 'password', 'sex', 'age']

USER_ENUM = {
    'id': 0,
    'firstName': 1,
    'lastName': 2,
    'sex': 3,
    'age': 4,
    'email': 5,
    'password': 6,
    'description': 7,
    'weight': 8,
    'height': 9,
    'corpu': 10,
    'smoking': 11,
    'drink': 12,
    'diet': 13,
    'research': 14,
    'engagement': 15,
    'frequency': 16,
    'numberPhoto': 17,
}
LIST_SEX = ['M', 'F']
MIN_AGE = 15
MAX_AGE = 80

# pour la categorie santé
LIST_DRINK = ['never', 'occasionally', 'often', 'very often']
LIST_DIET = ['vegetarian', 'vegan', 'carnivore', 'omnivore', 'rich in protein']

# pour la categorie corps
MAX_WEIGHT = 300
MIN_WEIGHT = 40
MAX_HEIGHT = 220
MIN_HEIGHT = 90
LIST_CORPU = ['thin', 'normal', 'athletic', 'fat']

# pour la categorie relation ideale
LIST_RESEARCH = ['friendly meeting', 'serious relationship', 'no idea']
LIST_ENGAGEMENT = ['short term', 'long term', 'no idea']
LIST_FREQUENCY = ['Daily', 'Weekly', 'Occassional', 'other']