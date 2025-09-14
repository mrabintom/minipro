from flask import Blueprint, render_template

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/')
def dashboard():
    return render_template('student.html')

# Add more student routes as needed
