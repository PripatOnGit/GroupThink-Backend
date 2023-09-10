from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import hashlib
import db
from datetime import datetime


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/api/auth/signup", methods= ['POST'])
def signup():    
    data = request.get_json()  
    data["joinedAt"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    db.write_row(data)
    return jsonify("Success !!"),200


@app.route("/api/user/checkUsernameAvailability", methods= ['GET'])
def checkUserAvailability():
    username = request.args.get("username")
    print("checking username =>", username)
    data_lst = db.read_all_rows()    
    for row in data_lst:
        if row["username"] == username:            
            return jsonify(False), 200
    return jsonify(True), 200


@app.route("/api/user/checkEmailAvailability", methods= ['GET'])
def checkEmailAvailability():
    email = request.args.get("email")
    print("checking email =>", email)
    data_lst = db.read_all_rows()    
    for row in data_lst:
        if row["email"] == email:            
            return jsonify(False), 200
    return jsonify(True), 200


@app.route("/api/auth/signin", methods= ['POST'])
def login():    
    data = request.get_json()    
    data_lst = db.read_all_rows()    
    for row in data_lst:
        if (row["username"] == data["usernameOrEmail"] or row["email"] == data["usernameOrEmail"]) and row["password"] == data["password"]:            
            accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()
            return jsonify({"accessToken": accessToken}), 200
    return jsonify(False), 200


@app.route("/api/users/<username>", methods= ['GET'])
def user_by_name(username):        
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return jsonify("Unauthorized Access"), 401
    
    data_lst = db.read_all_rows()        
    for row in data_lst:
        accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()        
        if accessToken == authorization_header.split()[1]:            
            return jsonify({
                "name": row["name"],
                "username": row["username"],
                "joinedAt": row["joinedAt"],
                "pollCount": len(row["polls"]),
                "voteCount": 0
            }), 200
    return jsonify(False), 200


@app.route("/api/user/me", methods= ['GET'])
def user_me():        
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return jsonify("Unauthorized Access"), 401
    
    data_lst = db.read_all_rows()        
    for row in data_lst:
        accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()        
        if accessToken == authorization_header.split()[1]:            
            return jsonify({"username": row["username"]}), 200
    return jsonify(False), 200


@app.route("/api/polls", methods= ['GET'])
def get_polls():        
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return jsonify("Unauthorized Access"), 401
    
    data_lst = db.read_all_rows()        
    for row in data_lst:
        accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()        
        if accessToken == authorization_header.split()[1]:         
            for poll in row["polls"]:
                poll["createdBy"] = {"username": row["username"], "name": row["name"]}
            return jsonify({
                "content": row["polls"],
                "page": 1,
                "size": 1,
                "totalPages": 1,
                "totalElemets": 1,
                "last": 1                
            }), 200
    return jsonify(False), 200


@app.route("/api/users/<username>/polls", methods= ['GET'])
def get_polls_by_user(username):        
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return jsonify("Unauthorized Access"), 401
    
    data_lst = db.read_all_rows()        
    for row in data_lst:
        accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()        
        if accessToken == authorization_header.split()[1]:         
            for poll in row["polls"]:
                poll["createdBy"] = {"username": row["username"], "name": row["name"]}
            return jsonify({
                "content": row["polls"],
                "page": 1,
                "size": 1,
                "totalPages": 1,
                "totalElemets": 1,
                "last": 1                
            }), 200
    return jsonify(False), 200


@app.route("/api/polls", methods= ['POST'])
def submit_polls():        
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return jsonify("Unauthorized Access"), 401
    
    poll = request.get_json()
    poll["creationDateTime"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    data_lst = db.read_all_rows()        
    for row in data_lst:
        accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()        
        if accessToken == authorization_header.split()[1]:
            row.get("polls", []).append(poll)
            db.update_row(row)
            return jsonify(True), 200
    return jsonify(False), 200


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"