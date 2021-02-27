from cryptography.fernet import Fernet
from DataAccess import SqliteDatabase
import asyncio
from Crypto.Hash import SHA256


async def loginUser(id, password):
    isPasswordCorrect = await isPasswordCorrectForId(id, password)
    if isPasswordCorrect is False:
        return {"message": "password is wrong"}
    token = await SqliteDatabase.getToken(id)
    await SqliteDatabase.submitLogin(id, token)
    return {"message": "logged in successful", "token": token}


async def isPasswordCorrectForId(id, password):
    encryptedPassword = await SqliteDatabase.getPasswordForThisId(id)
    if encryptedPassword != encryptPassword(id, password):
        return False
    return True


async def isTokenExpired(token):
    isExpired = SqliteDatabase.isTokenExpired(token)
    return {"isExpired": isExpired}


async def registerUser(id, password):
    encryptedPassword = encryptPassword(id, password)
    await SqliteDatabase.registerUser(id, encryptedPassword)
    return {"message": "register successful"}


def encryptPassword(id, password):
    hash = SHA256.new(id.encode('utf-8'))
    hash.update(password.encode('utf-8'))
    return hash.digest()


async def getUserIdWithToken(token):
    userId = await SqliteDatabase.getUserIdWithToken(token)
    return {"id": userId}


async def runDatabase(path):
    SqliteDatabase.usersDb = await SqliteDatabase.openUsersDatabase(path)
    SqliteDatabase.loginsLogDb = await SqliteDatabase.openLoginsLogDatabase(path)
    await SqliteDatabase.createLoginsLogTable()
    await SqliteDatabase.createUsersTable()
    await SqliteDatabase.printLoginsLogTable()
    await SqliteDatabase.printUsersTable()

# if __name__ == "__main__":
#     asyncio.run(runDatabase("../DataAccess/DB/"))
#     messag = asyncio.run(loginUser("alirezaaa", "heidari"))
#     print(messag)
#     asyncio.run(SqliteDatabase.printLoginsLogTable())
