from flask import Flask, redirect, url_for, request, jsonify
import json
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
        return jsonify(responseData)


async def runServer():
    print("1")
    await ServerController.runDatabase("../DataAccess/DB/")
    print("2")
    await app.run(host="localhost", port=9000, debug=False)
    print(3)


if __name__ == '__main__':
    asyncio.run(runServer())
