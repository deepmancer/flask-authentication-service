from data_access import database
from Crypto.Hash import SHA256
import jwt
from datetime import *


async def loginUser(id, password):
    isThisUserExists = await database.isThereUserWithId(id)
    if isThisUserExists is False:
        return {"message": "no users with this id", "token": None}

    isPasswordCorrect = await isPasswordCorrectForId(id, password)
    if isPasswordCorrect is False:
        return {"message": "password is wrong", "token": None}
    token = await getToken(id)
    await database.submitLogin(id, token)
    return {"message": "login successful", "token": token}


async def isPasswordCorrectForId(id, password):
    encryptedPassword = await database.getPasswordForThisId(id)
    if encryptedPassword != encryptPassword(id, password):
        return False
    return True


async def isTokenExpired(token):
    try:
        jwt.decode(token, "secret", algorithms=["HS256"])
        if await database.isThisTokenAvailable(token) is True:
            return False
        return True
    except Exception as e:
        return True


async def registerUser(id, password):
    isThisUserExists = await database.isThereUserWithId(id)
    if isThisUserExists is True:
        return {"message": "you can not register"}

    encryptedPassword = encryptPassword(id, password)
    await database.registerUser(id, encryptedPassword)
    return {"message": "register successful"}


def encryptPassword(id, password):
    hash = SHA256.new(id.encode('utf-8'))
    hash.update(password.encode('utf-8'))
    return str(hash.digest())


async def getUserIdWithToken(token):
    userId = await database.getUserIdWithToken(token)
    return {"id": userId}


async def runDatabase():
    database.database = await database.connectToDatabases()
    print("connected to mongodb database")
    await database.printUsersCollection()
    await database.printLoginsLogCollection()


async def getToken(id):
    userLastToken = await database.getUserLastToken(id)
    if await isTokenExpired(userLastToken) is False:
        return userLastToken

    token = getNewToken(id)
    return token


def getNewToken(id):
    currentTime = datetime.utcnow()
    deltaTime = timedelta(hours=10)
    expirationTime = currentTime + deltaTime
    token = jwt.encode({"exp": expirationTime, "id": id}, "secret")
    return str(token)
