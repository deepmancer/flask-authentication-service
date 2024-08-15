from data_access import database
from Crypto.Hash import SHA256
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"

async def login_user(user_id, password):
    user_exists = await database.does_user_exist(user_id)
    if not user_exists:
        return {"message": "No user with this ID", "token": None}

    if not await is_password_correct(user_id, password):
        return {"message": "Incorrect password", "token": None}

    token = await get_or_create_token(user_id)
    await database.record_login(user_id, token)
    return {"message": "Login successful", "token": token}

async def is_password_correct(user_id, password):
    stored_password = await database.get_password(user_id)
    return stored_password == encrypt_password(user_id, password)

async def is_token_expired(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return not await database.is_token_valid(token)
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        return True

async def register_user(user_id, password):
    if await database.does_user_exist(user_id):
        return {"message": "User already exists"}

    encrypted_password = encrypt_password(user_id, password)
    await database.register_user(user_id, encrypted_password)
    return {"message": "Registration successful"}

def encrypt_password(user_id, password):
    hash = SHA256.new(user_id.encode('utf-8'))
    hash.update(password.encode('utf-8'))
    return hash.hexdigest()

async def get_user_id_with_token(token):
    user_id = await database.get_user_id_by_token(token)
    return {"id": user_id}

async def initialize_database():
    await database.connect()
    print("Connected to MongoDB")
    await database.print_users_collection()
    await database.print_logins_collection()

async def get_or_create_token(user_id):
    last_token = await database.get_last_token(user_id)
    if last_token and not await is_token_expired(last_token):
        return last_token
    return generate_token(user_id)

def generate_token(user_id):
    expiration_time = datetime.utcnow() + timedelta(hours=10)
    return jwt.encode({"exp": expiration_time, "id": user_id}, SECRET_KEY, algorithm="HS256")
