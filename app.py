import pg

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
    user_not_found = pg.check_user_availability("username", username)    
    return jsonify(user_not_found), 200


@app.route("/api/user/checkEmailAvailability", methods= ['GET'])
def checkEmailAvailability():
    email = request.args.get("email")
    print("checking email =>", email)
    user_not_found = pg.check_user_availability("email", email)    
    return jsonify(user_not_found), 200