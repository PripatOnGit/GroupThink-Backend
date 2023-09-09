from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import json
import db

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/api/auth/signup", methods= ['POST'])
def signup():
    print("this is fun !!")
    data = request.get_json()
    #print(data)
    db.write(data)
    return jsonify("Success !!"),200

@app.route("/api/user/checkUsernameAvailability", methods= ['GET'])
def checkUserAvailability():
    data = request.args.get("username", default=None, type=None)
    print(data)
    data_records = db.read()
    for index in range(len(data_records)):
        for key in data_records[index]:
            if data == data_records[key]:
                print("Username is already taken !!")
                break
        else:
            continue
    return  jsonify("Success !!")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"