from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/militar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'Person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(80))
    ideology = db.Column(db.String(80))

    def __init__(self, name, surname, nickname=None, ideology=None):
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.ideology = ideology

    def prettyPrint(self):
        return "name: ", self.name, " surname: ", self.surname, " nickname: ", self.nickname, " ideology: ", self.ideology
    

@app.route("/load")
def load():
    #some trial data
    person1 = Person("Chavo", "Tritones")
    person2 = Person("Sebastian", "Pose", "sebita", "Kishnerista")
    person3 = Person("Budy", "Andy", None ,"Peronista")
    db.session.add(person1)
    db.session.add(person2)
    db.session.add(person3)
    db.session.commit()
    print(person1.prettyPrint())
    print(person2.prettyPrint())
    print(person3.prettyPrint())
    return "fueron agregados"

@app.route("/allPersons", methods=['GET'])
def getAllPersons():
    #/allPersons return all persons in database
    try:
        all = Person.query.all()
        resp = {}
        i = 0
        for person in all:
            parcial = {}
            parcial['id'] = person.id
            parcial['name'] =  person.name
            parcial['surname'] =  person.surname
            parcial['nickaname'] =  person.nickname
            parcial['ideology'] =  person.ideology
            resp[i] = parcial
            i = i + 1
        return jsonify(resp), 200
    except:
        return ""

@app.route("/person/<person_id>", methods=['GET'])
def getOnePerson(person_id):
    #/person/<person_id> return a person in database that matches the id passed by parameter
    try:
        person = Person.query.filter_by(id=person_id).first()
        resp = {}
        resp['id'] = person.id
        resp['name'] =  person.name
        resp['surname'] =  person.surname
        resp['nickaname'] =  person.nickname
        resp['ideology'] =  person.ideology
        return jsonify(resp), 200
    except:
        return jsonify({'message' : 'Person id not found!'}), 404

@app.route("/person/create", methods=['POST'])
def createPerson():
    #/person/create create new person in database. receives a json like => (body) {"name" : "america","surname" : "latina", "nickname" : null, "ideology" : "troskista" }
    try:
        json = request.get_json()
        newPerson = Person(json['name'], json['surname'], json['nickname'], json['ideology'])
        db.session.add(newPerson)
        db.session.commit()
        return jsonify({'message' : 'New person has been created!'}), 200
    except:
        return ""

@app.route("/person/edit/<person_id>", methods=['PUT'])
def editPerson(person_id):
    #/person/edit/<person_id> edit a person in database, receives a json like => (body)  {"name" : "america","surname" : "latina", "nickname" : null, "ideology" : "troskista" }
    try:
        person = Person.query.filter_by(id=person_id).first()
        json = request.get_json()
        person.name = json['name'] 
        person.surname = json['surname'] 
        person.nickname = json['nickname'] 
        person.ideology = json['ideology'] 
        db.session.commit()
        return jsonify({'message' : 'Person has been modified!'}), 200
    except:
        return jsonify({'message' : 'Person id not found!'}), 404

@app.route("/person/delete/<person_id>", methods=['DELETE'])
def deletePerson(person_id):
    #/person/delete/<person_id> delete a person in database that matches the id passed by parameter
    try:
        person = Person.query.filter_by(id = person_id).first()
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'The person has been deleted!'}), 200
    except:
        return jsonify({'message' : 'Person id not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)