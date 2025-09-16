from flask import Blueprint, render_template
from backend.models import db, Admin, Teacher, Student, Attendance, Fine

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/')
def dashboard():
    return render_template('student.html')

@student_bp.route('/profile/<int:student_id>')
def profile(student_id):
    student = Student.query.get(student_id)
    return render_template('student_profile.html', student=student)

# Add more student routes as needed

from backend.student import student_bp
app.register_blueprint(student_bp, url_prefix='/student')
