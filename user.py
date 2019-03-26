from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, session, make_response
from flask_wtf import CsrfProtect
from flask_cors import CORS
import time
import MySQLdb
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/militar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, name, password, username):
        self.name = name
        self.password = password
        self.username = username

@app.route("/user/load")
def load():
    #some trial data
    user1 = User("Chavo", "Tritones", "chaveta")
    user2 = User("Sebastian", "Pose", "sebita")
    user3 = User("Budy", "Andy","Peronista")
    user4 = User("zeqe", "boris", "macrista")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()
    return "fueron agregados"


@app.route("/login", methods=['POST'])
def login():
    #sign in -> set cookie and session
    try:
        json = request.get_json()
        user = User.query.filter_by(username=json['username']).first()       
        if json['password'] == user.password and json['username'] == user.username:
            session['logged_in'] = True
            session['username'] = user.username
            response = make_response()
            response.set_cookie('council', str(user.id))
            print(response.cookies.get('council'))
            return response
#            return jsonify({'message' : 'session started', 'session' : session['username']}), 200
        else:
            return jsonify({'message' : 'incorrect username or password'}), 400
    except:
        return jsonify({'message' : 'not found'}), 405


@app.route("/logout", methods=['GET'])
def logout():
    #sing out -> destroy session
    try:
        response = make_response()
        response.set_cookie('council', expires=0)
        session.pop('username')
        return jsonify({'message' : 'session close'}), 200
    except:
        return jsonify({'message' : 'no session open'}), 400

@app.route("/user/create", methods=['POST'])
def createUser():
    #/user/create create a new user in database. receives a json like => 
    try:
        json = request.get_json()
        newUser = User(json['name'], json['password'], json['username'])
        db.session.add(newUser)
        db.session.commit()
        return jsonify({'message' : 'New user has been created!'}), 200
    except:
        return jsonify({'message' : 'bad request'}), 400

@app.route("/user/delete/<user_id>", methods=['DELETE'])
def deleteUser(user_id):
    #/user/delete/<user_id> delete an user in database that matches the id passed by parameter
    try:
        user = User.query.filter_by(id = user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'The user has been deleted!'}), 200
    except:
        return jsonify({'message' : 'User id not found!'}), 404

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)