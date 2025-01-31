from database import createElem, getElems, deleteTableContent, deleteElem
from models import User
import os
from pathlib import Path

LIST_INTERESTS = open(Path(__file__).parent.parent / 'config' / 'interests.txt', 'r', encoding='utf-8').read().split('\n')

class UserInterests:
    table_name = 'user_interests'
    columns = {
        'user_id': 'INT NOT NULL',
        'interest_id': 'INT NOT NULL',
        'PRIMARY KEY (user_id, interest_id)': '',
        'FOREIGN KEY (user_id)': 'REFERENCES users(id) ON DELETE CASCADE',
        'FOREIGN KEY (interest_id)': 'REFERENCES interests(id) ON DELETE CASCADE',
    }

class interests:
    table_name = 'interests'
    columns = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(50) NOT NULL',
    }

def init_interests():
    inter = getElems(interests)
    interNames = [elem[1] for elem in inter]
    if len(inter) > 0:
        for interest in inter:
            if (interest[1] not in LIST_INTERESTS):
                deleteElem(interests, {'id': interest[0]})
        for interest in LIST_INTERESTS:
            if interest not in interNames:
                createElem(interests, {'name': interest})
            
    else:
        for interest in LIST_INTERESTS:
            createElem(interests, {'name': interest})

def modifyUserInterest(userEmail, interestName):
    interest = getElems(interests, {'name': interestName})
    if len(interest) == 0:
        raise Exception('Interest not found')
    interest = interest[0]
    users = getElems(User, {'email': userEmail})
    if len(users) == 0:
        raise Exception('User not found')
    user = users[0][0]
    createElem(UserInterests, {'user_id': user, 'interest_id': interest[0]}, ['user_id', 'interest_id'])

def getAllUsersInterest(userEmail):
    users = getElems(User, {'email': userEmail})
    if len(users) == 0:
        raise Exception('User not found')
    user = users[0]
    usersInterests = getElems(UserInterests, {'user_id': user[0]})
    temp = []
    for interest in usersInterests:
        gettedInterest = getElems(interests, {'id': interest[1]})
        temp.append(gettedInterest[0][1])
    usersInterests = temp
    if len(usersInterests) == 0:
        return []
    return usersInterests

def getAllInterestsUsers(interestName):
    interest = getElems(interests, {'name': interestName})
    if len(interest) == 0:
        raise Exception('Interest not found')
    interest = interest[0]
    usersInterests = getElems(UserInterests, {'interest_id': interest[0]})
    temp = []
    for user in usersInterests:
        gettedUser = getElems(User, {'id': user[0]})
        temp.append(gettedUser[0][1])
    usersInterests = temp
    if len(usersInterests) == 0:
        return []
    return usersInterests
    
