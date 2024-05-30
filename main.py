from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

# Configure the database URI. Replace 'username', 'password', 'hostname', 'port', and 'database_name' with your actual database credentials.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.getenv("DBUser") + ":" + os.getenv("DBPassword") + "@" + os.getenv("DBServer") + ":" + os.getenv("DBPort") + "/" + os.getenv("DBName")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Entry(db.Model):
    __tablename__ = 'next_events'

    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Description = db.Column(db.String(100))
    Location = db.Column(db.String(50))
    Day = db.Column(db.Integer)
    Month = db.Column(db.String(3))
    Time = db.Column(db.String(50))
    ImageLink = db.Column(db.String(150))
    State = db.Column(db.Integer, default=0)

# Create tables if not exists
with app.app_context():
    db.create_all()

# Authentication decorator
def createtoken_required(f):
    def createdecorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # You can implement your own token verification logic here
        if token != os.getenv("CreateToken"):
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return createdecorated


def deletetoken_required(f):
    def deletedecorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # You can implement your own token verification logic here
        if token != os.getenv("DeleteToken"):
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return deletedecorated

def gettoken_required(f):
    def getdecorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # You can implement your own token verification logic here
        if token != os.getenv("GetToken"):
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return getdecorated

# Endpoint to create a new entry
@app.route('/api/event/create', methods=['POST'])
@createtoken_required
def create_entry():
    data = request.get_json()

    new_entry = Entry(
        Name=data['name'],
        Description=data['description'],
        Location=data['location'],
        Day=data['day'],
        Month=data['month'],
        Time=data['time'],
        ImageLink=data['image_link']
    )

    with app.app_context():
        try:
            db.session.add(new_entry)
            db.session.commit()
            return jsonify({'message': 'Entry created successfully!'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while creating the entry. Please check your data.'}), 400


# Endpoint to delete an entry
@app.route('/api/event/delete/<int:entry_id>', methods=['DELETE'])
@deletetoken_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return jsonify({'message': 'Entry not found!'}), 404

    entry.State = 255
    try:
        db.session.commit()
        return jsonify({'message': 'Entry deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the entry.'}), 500

# Endpoint to retrieve all entry IDs with status equal to 0, along with their Name and Location
@app.route('/api/event/getall', methods=['GET'])
@gettoken_required
def get_entries():
    try:
        entries = Entry.query.filter_by(State=0).all()
        entry_list = [
            {
                'id': entry.Id,
                'friendlyText': f"Nummer: {entry.Id} | {entry.Name} in {entry.Location} am {entry.Day}.{entry.Month}"
            }
            for entry in entries
        ]
        return jsonify({'entries': entry_list}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving entries.'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
