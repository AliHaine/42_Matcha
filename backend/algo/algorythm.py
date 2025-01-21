from database import *
from models import *
from config import USER_ENUM

def getMatchableUsers(user, numberOfUsers=8):
    users = getElems(User, suppressEmpty=True);
    user = getElems(User, {"id": user})[0]
    usersWithoutUser = []
    for userFind in users:
        if user[USER_ENUM['id']] != userFind[USER_ENUM['id']]:
            usersWithoutUser.append(userFind)
    usersWithoutUser = convertToPublicProfiles(usersWithoutUser)
    print("\n\n\nusersWithoutUser")
    print(usersWithoutUser)
    if len(usersWithoutUser) < numberOfUsers:
        return usersWithoutUser
    return usersWithoutUser[:numberOfUsers]