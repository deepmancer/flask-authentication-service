from flask import Flask, request, jsonify
from Model import ServerController
import asyncio

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        responseData = asyncio.run(ServerController.loginUser(data["id"], data["password"]))
        return jsonify(responseData)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        responseData = asyncio.run(ServerController.registerUser(data["id"], data["password"]))
        return jsonify(responseData)


@app.route('/getUserIdWithToken', methods=['POST'])
def getId():
    if request.method == 'POST':
        data = request.get_json()
        responseData = asyncio.run(ServerController.getUserIdWithToken(data["token"]))
        return jsonify(responseData)


@app.route('/isTokenExpired', methods=['POST'])
def checkTokenExpired():
    if request.method == 'POST':
        data = request.get_json()
        responseData = asyncio.run(ServerController.isTokenExpired(data["token"]))
        finalResponse = str(responseData)
        return jsonify({"isExpired": finalResponse})


async def runServer():
    await ServerController.runDatabase()
    await app.run(host="localhost", port=9999, debug=False)


if __name__ == '__main__':
    asyncio.run(runServer())
