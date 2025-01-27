from .userGlobal import *
import pkgutil
import sys

# __all__ = ['ALLOWED_CHARACTERS', 'PASSWORD_REQUIREMENTS', 'REQUIRED_FIELDS', 'USER_ENUM', 'LIST_SEX', 'MIN_AGE', 'MAX_AGE', 'MAX_POIDS', 'MIN_POIDS', 'MAX_TAILLE', 'MIN_TAILLE', 'LIST_CORPU', 'LIST_BOIT', 'LIST_ALIM', 'LIST_RECHERCHE', 'LIST_ENGAGEMENT', 'LIST_FREQUENCE']
__all__ = []
# Dynamically import all modules in the current package
# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     __import__(module_name)

# Dynamically add all variables from the imported modules to __all__
current_module = sys.modules[__name__]
for attr in dir(current_module):
    if not attr.startswith("__"):
        __all__.append(attr)