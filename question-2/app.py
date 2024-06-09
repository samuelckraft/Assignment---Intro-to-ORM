#Task 1
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:654U7jsv@localhost/fitness_center'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    trainer_id = db.Column(db.String(100), nullable = False)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/trainers', methods = ['GET'])
def get_trainers():
    trainers = db.session.query(Member.trainer_id).distinct().all()
    unique_ids = [trainer_id for (trainer_id, ) in trainers]
    return jsonify(unique_ids)



#Task 2
@app.route('/membercount', methods = ['GET'])
def member_count():
    members = db.session.query(Member.trainer_id, db.func.count(Member.id)).group_by(Member.trainer_id).all()
    trainer_count = [(trainer_id, count) for trainer_id, count in members]
    return jsonify(trainer_count)

#Task 3
@app.route('/between', methods = ["GET"])
def members_between():
    members = db.session.query(Member).filter(Member.age.between(25,30)).all()
    member_info = [{'name': member.name, 'age': member.age, 'trainer_id': member.trainer_id} for member in members]
    return jsonify(member_info)