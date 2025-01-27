# pour la creation d'un utilisateur
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
    'description': 7,
    'poids': 8,
    'taille': 9,
    'corpulence': 10,
    'fumeur': 11,
    'boit': 12,
    'alimentation': 13,
    'recherche': 14,
    'engagement': 15,
    'frequence': 16,
    'numberPhoto': 17,
}
LIST_SEXE = ['H', 'F']
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
LIST_CORPU = ['thin', 'normal', 'athletic', 'fort']

# pour la categorie relation ideale
LIST_RECHERCHE = ['friendly meeting', 'serious relationship', 'no idea']
LIST_ENGAGEMENT = ['court terme', 'long terme', 'aucune idee']
LIST_FREQUENCE = ['Quotidienne', 'Hebdomadaire', 'Occassionnelle', 'autre']