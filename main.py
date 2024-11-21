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
    TicketLink = db.Column(db.String(150), default='https://titankollektiv.de/tickets')
    State = db.Column(db.Integer, default=0)

# Create tables if not exists
with app.app_context():
    db.create_all()

# Endpoint to retrieve all entryss with status equal to 0
@app.route('/api/v2/event/get/active', methods=['GET'])
def get_entries_active():
    try:
        entries = Entry.query.filter_by(State=0).all()
        entry_list = [
            {
                'id': entry.Id,
                'name': entry.Name,
                'location': entry.Location,
                'day': entry.Day,
                'monthString': entry.Month,
                'friendlyText': f"Nummer: {entry.Id} | {entry.Name} in {entry.Location} am {entry.Day}.{entry.Month}"
            }
            for entry in entries
        ]
        return jsonify({'entries': entry_list}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving entries.'}), 500

# Endpoint to retrieve all entrys with status equal to 255
@app.route('/api/v2/event/get/inactive', methods=['GET'])
def get_entries_inactive():
    try:
        entries = Entry.query.filter_by(State=255).all()
        entry_list = [
            {
                'id': entry.Id,
                'name': entry.Name,
                'location': entry.Location,
                'day': entry.Day,
                'monthString': entry.Month,
                'friendlyText': f"Nummer: {entry.Id} | {entry.Name} in {entry.Location} am {entry.Day}.{entry.Month}"
            }
            for entry in entries
        ]
        return jsonify({'entries': entry_list}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving entries.'}), 500

# Endpoint to retrieve all entrys
@app.route('/api/v2/event/get/all', methods=['GET'])
def get_entries_all():
    try:
        entries = Entry.query.all()
        entry_list = [
            {
                'id': entry.Id,
                'name': entry.Name,
                'location': entry.Location,
                'day': entry.Day,
                'monthString': entry.Month,
                'friendlyText': f"Nummer: {entry.Id} | {entry.Name} in {entry.Location} am {entry.Day}.{entry.Month}"
            }
            for entry in entries
        ]
        return jsonify({'entries': entry_list}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving entries.'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
