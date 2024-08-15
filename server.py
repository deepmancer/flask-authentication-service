from flask import Flask, request, jsonify
from model import controller

app = Flask(__name__)

@app.post('/login')
async def login():
    data = request.get_json()
    response_data = await controller.login_user(data["id"], data["password"])
    return jsonify(response_data)

@app.post('/register')
async def register():
    data = request.get_json()
    response_data = await controller.register_user(data["id"], data["password"])
    return jsonify(response_data)

@app.post('/getUserIdWithToken')
async def get_user_id_with_token():
    data = request.get_json()
    response_data = await controller.get_user_id_with_token(data["token"])
    return jsonify(response_data)

@app.post('/isTokenExpired')
async def is_token_expired():
    data = request.get_json()
    is_expired = await controller.is_token_expired(data["token"])
    return jsonify({"isExpired": is_expired})

async def run_server():
    await controller.initialize_database()
    await app.run_task(host="localhost", port=9999, debug=False)

if __name__ == '__main__':
    import asyncio
    asyncio.run(run_server())
