from flask import Blueprint, render_template

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/')
def dashboard():
    return render_template('teacher.html')

# Add more teacher routes as needed
