import pg, hashlib, uuid

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/")
def index():
    return "<p>Default Response</p>"


@app.route("/api/auth/signup", methods= ['POST'])
def signup():    
    data = request.get_json()  
    success = pg.create_user(data)
    if success:
        return jsonify("Success !!"), 200
    return jsonify("Failed to create user"), 500


@app.route("/api/user/checkUsernameAvailability", methods= ['GET'])
def checkUserAvailability():
    username = request.args.get("username")
    print("checking username =>", username)
    user_found = pg.search_user("username", username)    
    user_not_found = None if not user_found else False
    return jsonify(user_not_found), 200


@app.route("/api/user/checkEmailAvailability", methods= ['GET'])
def checkEmailAvailability():
    email = request.args.get("email")
    print("checking email =>", email)
    user_found = pg.search_user("email", email)  
    user_not_found = None if not user_found else False  
    return jsonify(user_not_found), 200


# @app.route("/api/auth/signin", methods= ['POST'])
# def login():    
#     data = request.get_json()    
#     data_lst = json_db.read_all_rows()    
#     for row in data_lst:
#         if (row["username"] == data["usernameOrEmail"] or row["email"] == data["usernameOrEmail"]) and row["password"] == data["password"]:            
#             accessToken = hashlib.md5("{0}__{1}".format(row["username"], row["password"]).encode()).hexdigest()
#             return jsonify({"accessToken": accessToken}), 200
#     return jsonify(None), 200


@app.route("/api/auth/signin", methods= ['POST'])
def login():    
    data = request.get_json()
    users = pg.search_user("username", data["usernameOrEmail"])
    if not users:
        users = pg.search_user("email", data["usernameOrEmail"])
    if not users:    
        return None
    #check for password match
    hashed_password = users[0][4]
    input_password = hashlib.md5(data["password"].encode()).hexdigest()
    if hashed_password == input_password:
        accessToken = hashlib.md5("{0}__{1}".format(users[0][3], uuid.uuid4()).encode()).hexdigest()
        return jsonify({"accessToken": accessToken}), 200
    return jsonify(None), 200
    