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

# Show All Records (Same as Read but separate route)
@app.route('/students/showall', methods=['GET'])
def show_all_students():
    students = session.query(StudentProfile).all()
    all_students = [
        {
            "ID": s.student_id,
            "Full Name": f"{s.first_name} {s.last_name}",
            "DOB": str(s.dob),
            "Due Amount": s.amount_due
        } for s in students
    ]
    return jsonify({"All Students": all_students})

# Update (PUT)
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = session.query(StudentProfile).get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    if 'dob' in data:
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    student.amount_due = data.get('amount_due', student.amount_due)

    session.commit()
    return jsonify({"message": "Student updated successfully!"})

# Delete (DELETE)
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = session.query(StudentProfile).get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    session.delete(student)
    session.commit()
    return jsonify({"message": "Student deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
