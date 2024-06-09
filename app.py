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

class memberschema(ma.Schema):
    name = fields.String(required = True) 
    age = fields.Integer(required = True) 
    trainer_id = fields.String(required = True)
    

    class Meta:
        fields = ('name', 'age', 'trainer_id', 'id')

class sessionchema(ma.Schema):
    member_id = fields.Integer(required = True) 
    session_date = fields.Date(required = True) 
    session_time = fields.String(required = True)
    calories_burned = fields.Integer(required = True)
    

    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'session_time', 'calories_burned')

member_schema = memberschema()
members_schema = memberschema(many=True)

session_schema = sessionchema()
sessions_schema = sessionchema(many=True)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    trainer_id = db.Column(db.String(100), nullable = False)
    sessions = db.relationship('WorkoutSession', backref = 'Member', uselist = False)


class WorkoutSession(db.Model):
    __tablename__ = 'workoutsessions'
    session_id = db.Column(db.Integer, primary_key = True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    session_date = db.Column(db.Date)
    session_time = db.Column(db.String(50))
    calories_burned = db.Column(db.Integer)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/members', methods = ['GET'])
def get_customers():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods = ['POST'])
def add_customer():
    try:
        #validate and deserialize input
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_member = Member(name = member_data['name'], age = member_data['age'], trainer_id = member_data['trainer_id'])
    db.session.add(new_member)
    db.session.commit()

    return jsonify({'message': "New member added successfully"}), 201


@app.route('/members/<int:id>', methods = ['PUT'])
def update_customer(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    member.name = member_data['name']
    member.age = member_data['age']
    member.trainer_id = member_data['trainer_id']
    db.session.commit()

    return jsonify({'message': 'Member details updated succesfully'}), 200

@app.route('/members/<int:id>', methods = ['DELETE'])
def delete_customer(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": 'Member deleted successfully'}), 200



#Task 2

@app.route('/workoutsessions', methods = ['GET'])
def view_sessions():
    sessions = WorkoutSession.query.all()
    return sessions_schema.jsonify(sessions)

@app.route('/workoutsessions', methods = ['POST'])
def add_session():
    try:
        #validate and deserialize input
        session_data = session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_session = WorkoutSession(member_id = session_data['member_id'], session_date = session_data['session_date'], session_time = session_data['session_time'], calories_burned = session_data['calories_burned'])
    db.session.add(new_session)
    db.session.commit()

    return jsonify({'message': "New session added successfully"}), 201

@app.route('/workoutsessions/<int:id>', methods = ['PUT'])
def update_session(id):
    session = WorkoutSession.query.get_or_404(id)
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    session.member_id = session_data['member_id']
    session.session_date = session_data['session_date']
    session.session_time = session_data['session_time']
    session.calories_burned = session_data['calories_burned']

    db.session.commit()

    return jsonify({'message': 'Session details updated succesfully'}), 200

@app.route('/workoutsessions/<int:id>', methods = ['DELETE'])
def delete_session(id):
    sessions = WorkoutSession.query.get_or_404(id)
    db.session.delete(sessions)
    db.session.commit()

    return jsonify({"message": 'Session deleted successfully'}), 200