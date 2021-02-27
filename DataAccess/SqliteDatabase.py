import sqlite3
import asyncio
import jwt
from datetime import *
import time

usersDb = None
loginsLogDb = None


# ************* create user and login database and tables *************


async def openUsersDatabase(path):
    userConnection = sqlite3.connect(path + 'users.db', check_same_thread=False)
    print("Opened  users database successfully")
    return userConnection


async def openLoginsLogDatabase(path):
    loginConnection = sqlite3.connect(path + 'loginsLog.db', check_same_thread=False)
    print("Opened logins log database successfully")
    return loginConnection


async def createLoginsLogTable():
    try:

        asyncio.run(loginsLogDb.execute('''CREATE TABLE loginsLogTable
                   (loginCount INT PRIMARY KEY  NOT NULL,
                   id          TEXT             NOT NULL,
                   token       TEXT             NOT NULL);'''))
        print("logins log table created")
    except:
        print("logins log table already exists")


async def createUsersTable():
    try:
        asyncio.run(usersDb.execute('''CREATE TABLE  usersTable
                (id         TEXT PRIMARY KEY  NOT NULL,
                password    TEXT              NOT NULL);'''))
        print("users table created")
    except Exception as e:
        print("users table already exists")


async def printLoginsLogTable():
    try:
        cursor = loginsLogDb.cursor()
        table = cursor.execute("SELECT * FROM loginsLogTable").fetchall()
        print({"logins log table": table})

    except:
        print("can not print logins log table")


async def printUsersTable():
    try:
        cursor = usersDb.cursor()
        table = cursor.execute("SELECT * FROM usersTable").fetchall()
        print({"users table": table})
    except:
        print("can not print users table")


# ************* logins functions *************


async def submitLogin(userId, token):
    allIds = (loginsLogDb.execute('SELECT id from loginsLogTable WHERE 1 = 1')).fetchall()
    primaryKey = len(allIds) + 1
    values = (primaryKey, userId, token)
    loginsLogDb.execute(''' INSERT INTO loginsLogTable(loginCount,id,token) VALUES(?,?,?) ''', values)
    print("login submitted")
    loginsLogDb.commit()


def isTokenExpired(token):
    try:
        jwt.decode(token, "secret", algorithms=["HS256"])
        return "False"
    except Exception as e:
        return "True"


def getNewToken(id):
    currentTime = datetime.utcnow()
    deltaTime = timedelta(hours=1)
    expirationTime = currentTime + deltaTime
    token = jwt.encode({"exp": expirationTime, "id": id}, "secret")
    return token


async def getToken(id):
    token = None
    usersTokens = loginsLogDb.execute('SELECT token FROM loginsLogTable WHERE id = ?', (id,)).fetchall()

    for userTokenTuple in usersTokens:
        userToken = userTokenTuple[0]
        if isTokenExpired(userToken) == "False":
            token = userToken
            break

    if token is not None:
        return token

    token = getNewToken(id)
    return token


async def getUserIdWithToken(token):
    userId = 0
    try:
        userId = loginsLogDb.execute('SELECT id FROM loginsLogTable WHERE token = ?', (token,)).fetchone()[0]
    except:
        userId = None
    finally:
        return userId


# ************* user password stuff *************


async def getPasswordForThisId(id):
    encryptedPassword = ""
    try:
        encryptedPassword = usersDb.execute('SELECT password FROM usersTable WHERE id = ?', (id,)).fetchone()[0]
    except Exception as e:
        encryptedPassword = None
    finally:
        return encryptedPassword


async def registerUser(id, password):
    values = (id, password)
    usersDb.execute(''' INSERT INTO usersTable(id,password) VALUES(?,?) ''', values)
    usersDb.commit()


# if __name__ == "__main__":
#     usersDb = asyncio.run(openUsersDatabase("DB/"))
#     loginsLogDb = asyncio.run(openLoginsLogDatabase("DB/"))
#     #     #
#     asyncio.run(createLoginsLogTable())
    #     asyncio.run(createUsersTable())
    #     # asyncio.run(createLoginsLogTable())
    #     #
    #     values = ("ds", "heidari")
    #     usersDb.execute('''INSERT INTO usersTable (id,password) VALUES (?,?)''', values)
    #     usersDb.commit()
    #     asyncio.run(printUsersTable())
    #
    # token1 = asyncio.run(getToken("alireza"))
    # print(isTokenExpired(token1))
    # asyncio.run(submitLogin("alireza", token1))
    # time.sleep(1)
    # print(isTokenExpired(token1))
    # time.sleep(2.1)
    # print(isTokenExpired(token1))
    #
    # #     # asyncio.run(submitLogin("alireza", token1))
    # token2 = asyncio.run(getToken("alireza"))
    # asyncio.run(submitLogin("alireza", token2))
    # print(token1)
    # print(token2)
    # asyncio.run(printLoginsLogTable())
#     # asyncio.run(submitLogin("heidari", token2))
#     #
#     # time.sleep(2)
#     #
#     # token1 = asyncio.run(getToken("alireza"))
#     # asyncio.run(submitLogin("alireza", token1))
#     # token2 = asyncio.run(getToken("heidari"))
#     # asyncio.run(submitLogin("heidari", token2))
#     # time.sleep(4)
#     #
#     # token1 = asyncio.run(getToken("alireza"))
#     # asyncio.run(submitLogin("alireza", token1))
#     # token2 = asyncio.run(getToken("heidari"))
#     # asyncio.run(submitLogin("heidari", token2))
#     #
#     # # asyncio.run((submitLogin("asdf", "heidari")))
#     # # asyncio.run((submitLogin("doa", "abadi")))
#     #
#     # # tokenn = getNewToken("3");
#     # # print(isTokenExpired(tokenn))
#     # # time.sleep(3)
#     # # print(isTokenExpired(tokenn))
#     #
#     # # userI2d = asyncio.run(getUserIdWithToken("abadi"))
#     # # print(userI2d)
#     #
#     # asyncio.run(printLoginsLogTable())
#     print("hello")
