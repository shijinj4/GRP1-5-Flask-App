from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Db_creation import Base, StudentProfile
from datetime import datetime

app = Flask(__name__)

# Database setup
DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def home():
    return "Flask app is running! Database connected."

# Create (POST)
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = StudentProfile(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        amount_due=data['amount_due']
    )
    session.add(new_student)
    session.commit()
    return jsonify({"message": "Student added successfully!"}), 201

# Read (GET)
@app.route('/students', methods=['GET'])
def get_students():
    students = session.query(StudentProfile).all()
    student_list = [
        {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "dob": str(student.dob),
            "amount_due": student.amount_due
        }
        for student in students
    ]
    return jsonify(student_list)

if __name__ == "__main__":
    app.run(debug=True)
