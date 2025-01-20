from database import *
from models import *

def getMatchableUsers(user, numberOfUsers=8):
    users = getElems(User);
    userReturn = []
    for user in users:
        if user.email != user.email:
            userReturn.append(user)
    return userReturn