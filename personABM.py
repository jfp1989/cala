from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_wtf import CsrfProtect
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.secret_key = 'aSecretKey' #token validation
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/militar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'Person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(80))
    document = db.Column(db.Integer, unique=True, nullable=False)
    ideology = db.Column(db.String(80))
    ug = db.Column(db.Integer)

    def __init__(self, name, surname, document, nickname=None, ideology=None, ug=None):
        self.name = name
        self.surname = surname
        self.document = document
        self.nickname = nickname
        self.ideology = ideology
        self.ug = ug

@app.route("/person/load")
def load():
    #some trial data
    person1 = Person("Chavo", "Tritones", 888)
    person2 = Person("Sebastian", "Pose", 111, "sebita", "Kishnerista")
    person3 = Person("Budy", "Andy", 333, None ,"Peronista")
    person4 = Person("zeqe", "boris", 222,  None ,"macrista", 1)
    db.session.add(person1)
    db.session.add(person2)
    db.session.add(person3)
    db.session.add(person4)
    db.session.commit()
    return "fueron agregados"

@app.route("/allPersons", methods=['GET'])
def getAllPersons():
    #/allPersons return all persons in database
    try:
        all = Person.query.all()
        resp = []
        for person in all:
            parcial = {}
            parcial['id'] = person.id
            parcial['name'] =  person.name
            parcial['surname'] =  person.surname
            parcial['nickname'] =  person.nickname
            parcial['ideology'] =  person.ideology
            parcial['document'] = person.document
            parcial['ug'] =  person.ug
            resp.append(parcial)
        return jsonify(resp), 200
    except:
        return jsonify({'message' : 'bad request'}), 400

@app.route("/person/<person_document>", methods=['GET'])
def getOnePerson(person_document):
    #/person/<person_document> return a person in database that matches the document passed by parameter
    try:
        person = Person.query.filter_by(document=person_document).first()
        resp = {}
        resp['id'] = person.id
        resp['name'] =  person.name
        resp['surname'] =  person.surname
        resp['nickaname'] =  person.nickname
        resp['ideology'] =  person.ideology
        resp['document'] = person.document
        resp['ug'] =  person.ug
        return jsonify(resp), 200
    except:
        return jsonify({'message' : 'Person document not found!'}), 404

@app.route("/person/create", methods=['POST'])
def createPerson():
    #/person/create create new person in database. receives a json like => (body) {"name" : "america","surname" : "latina", "nickname" : null, "ideology" : "troskista", "documento" : 222 }
    try:
        json = request.get_json()
        newPerson = Person(json['name'], json['surname'], json['document'], json['nickname'], json['ideology'], json['ug'])
        db.session.add(newPerson)
        db.session.commit()
        return jsonify({'message' : 'OK!'}), 200
    except:
        return jsonify({'message' : 'bad request'}), 400

@app.route("/person/edit/<person_id>", methods=['PUT'])
def editPerson(person_id):
    #/person/edit/<person_id> edit a person in database, receives a json like => (body)  {"name" : "america","surname" : "latina", "nickname" : null, "ideology" : "troskista" }
    try:
        person = Person.query.filter_by(id=person_id).first()
        json = request.get_json()
        person.name = json['name'] 
        person.surname = json['surname'] 
        person.document = json['document']
        person.nickname = json['nickname'] 
        person.ideology = json['ideology'] 
        person.ug = json['ug'] 
        db.session.commit()
        return jsonify({'message' : 'Person has been modified!'}), 200
    except:
        return jsonify({'message' : 'Person id not found!'}), 400

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