
from flask import Flask, jsonify, request, render_template, redirect, url_for
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

# =========================
# Web UI Routes
# =========================

@app.route('/')
def index():
    students = session.query(StudentProfile).all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        new_student = StudentProfile(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            dob=datetime.strptime(request.form['dob'], '%Y-%m-%d'),
            amount_due=request.form['amount_due']
        )
        session.add(new_student)
        session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update_student_web():
    if request.method == 'POST':
        student = session.query(StudentProfile).get(int(request.form['student_id']))
        if student:
            student.first_name = request.form['first_name']
            student.last_name = request.form['last_name']
            student.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
            student.amount_due = request.form['amount_due']
            session.commit()
        return redirect(url_for('index'))
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_student_web():
    if request.method == 'POST':
        student = session.query(StudentProfile).get(int(request.form['student_id']))
        if student:
            session.delete(student)
            session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html')

@app.route('/show')
def show_students_web():
    students = session.query(StudentProfile).all()
    return render_template('show.html', students=students)

@app.route('/read', methods=['GET', 'POST'])
def read_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student = session.query(StudentProfile).get(student_id)
        if student:
            return render_template('read.html', student=student)
        else:
            return render_template('read.html', error="Student not found.")
    return render_template('read.html')

# =========================
# API Routes
# =========================

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

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = session.query(StudentProfile).get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    session.delete(student)
    session.commit()
    return jsonify({"message": "Student deleted successfully!"})

# =========================
# Main Entry
# =========================

if __name__ == "__main__":
    app.run(debug=True)
