from pymongo import MongoClient
from mongoengine import Document, connect, IntField, StringField

DATABASE_URI = 'mongodb+srv://client:password1379@cluster0.pcb8q.mongodb.net/database?retryWrites=true&w=majority'

class LoginLog(Document):
    logins_count = IntField(required=True)
    user_id = StringField(required=True)
    token = StringField(required=True)
    meta = {'collection': 'loginLogs'}

class RegisterLog(Document):
    user_id = StringField(required=True)
    password = StringField(required=True)
    meta = {'collection': 'users'}

async def connect():
    connect('database', host=DATABASE_URI)

async def print_logins_collection():
    print("********** Logins Collection **********")
    for log in LoginLog.objects:
        print(f"Logins Count: {log.logins_count} | User ID: {log.user_id} | Token: {log.token}")

async def print_users_collection():
    print("********** Users Collection **********")
    for user in RegisterLog.objects:
        print(f"User ID: {user.user_id} | Password: {user.password}")

async def record_login(user_id, token):
    log_count = LoginLog.objects.count()
    LoginLog(logins_count=log_count + 1, user_id=user_id, token=token).save()
    print("Login recorded")

async def get_last_token(user_id):
    logs = LoginLog.objects(user_id=user_id).order_by('-logins_count')
    return logs.first().token if logs else None

async def get_user_id_by_token(token):
    log = LoginLog.objects(token=token).first()
    return log.user_id if log else None

async def get_password(user_id):
    user = RegisterLog.objects(user_id=user_id).first()
    return user.password if user else None

async def is_token_valid(token):
    return LoginLog.objects(token=token).count() > 0

async def does_user_exist(user_id):
    return RegisterLog.objects(user_id=user_id).count() > 0

async def register_user(user_id, password):
    RegisterLog(user_id=user_id, password=password).save()
