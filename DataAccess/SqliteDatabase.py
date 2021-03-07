import asyncio
import sys
from pymongo import MongoClient
import srvlookup
from mongoengine import *
import dns.resolver

database = None


# ************* create user and login database and tables *************

class LoginLog(Document):
    loginsCount = IntField(required=True)
    userId = StringField(required=True)
    token = StringField(required=True)
    meta = {'collection': 'loginLogs'}


class RegisterLog(Document):
    userId = StringField(required=True)
    password = StringField(required=True)
    meta = {'collection': 'users'}


async def connectToDatabases():
    return connect('database',
                   host='mongodb+srv://client:password1379@cluster0.pcb8q.mongodb.net/database?retryWrites=true&w'
                        '=majority')


async def printLoginsLogCollection():
    try:
        print("********** logins log collection **********\n")
        for loginLogObject in LoginLog.objects:
            print(
                "loginsCount: " + str(loginLogObject.loginsCount) + " | userId: " + loginLogObject.userId + " | token: "
                + loginLogObject.token + " \n")

    except:
        print("can not print logins log collection")


async def printUsersCollection():
    try:
        print("********** users collection **********")
        for registerObject in RegisterLog.objects:
            print("userId: " + registerObject.userId + " | password: " + str(registerObject.password) + "\n")

    except:
        print("can not print users collection")


# ************* logins functions *************


async def submitLogin(userId, token):
    loginsCount = len(LoginLog.objects)
    primaryKey = loginsCount + 1
    loginLog = LoginLog(loginsCount=primaryKey, userId=userId, token=token).save()
    print("login submitted")


async def getUserLastToken(id):
    try:
        userTokens = (LoginLog.objects(userId=id))
        userLastToken = userTokens[len(userTokens) - 1].token
        return userLastToken
    except:
        return None


async def getUserIdWithToken(token):
    try:
        userId = LoginLog.objects(token=token)[0].userId
        return userId
    except:
        return None


# ************* user password stuff *************


async def getPasswordForThisId(id):
    try:
        encryptedPassword = RegisterLog.objects(userId=id)[0].password
        return encryptedPassword
    except:
        return None


async def isThisTokenAvailable(token):
    try:
        if len(LoginLog.objects(token=token)) != 0:
            return True
        return False
    except:
        return False


async def isThereUserWithId(id):
    try:
        user = RegisterLog.objects(userId=id)[0]
        return True
    except:
        return False


async def registerUser(id, password):
    user = RegisterLog(userId=id, password=password).save()

