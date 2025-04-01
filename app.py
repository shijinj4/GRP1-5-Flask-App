from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Db_creation import Base, StudentProfile  # Import from Db_creation

app = Flask(__name__)

# Connect to the existing database
DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def home():
    return "Flask app is running! Database connected."

# ✅ New route: Fetch all students (READ operation)
@app.route('/students', methods=['GET'])
def get_students():
    students = session.query(StudentProfile).all()
    student_list = [
        {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "dob": str(student.dob),  # Convert date to string
            "amount_due": student.amount_due
        }
        for student in students
    ]
    return jsonify(student_list)

if __name__ == "__main__":
    app.run(debug=True)
