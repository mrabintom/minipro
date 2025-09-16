from flask import Flask, render_template, request, redirect, url_for, session, flash
from backend.models import db, Admin, Teacher, Student, Attendance, Fine
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecret"

# Set config directly
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin%40123@localhost:5432/minipro"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Admin login
        user = Admin.query.filter_by(email=email, password=password).first()
        if user:
            session['role'] = 'admin'
            session['name'] = user.name
            return redirect(url_for('admin_dashboard'))

        # Teacher login
        teacher = Teacher.query.filter_by(email=email, password=password).first()
        if teacher:
            session['role'] = 'teacher'
            session['name'] = teacher.name
            session['teacher_id'] = teacher.teacher_id
            return redirect(url_for('teacher_dashboard'))

        # Student login
        student = Student.query.filter_by(email=email, password=password).first()
        if student:
            session['role'] = 'student'
            session['name'] = student.name
            session['student_id'] = student.student_id
            return redirect(url_for('student_dashboard'))

        return render_template('login.html', message="Invalid credentials")
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    teachers = Teacher.query.all()
    students = Student.query.all()
    fines = Fine.query.all()
    return render_template("admin.html", 
                           name=session.get("name"),
                           email=session.get("email"),
                           teachers=teachers,
                           students=students,
                           fines=fines)

@app.route('/teacher')
def teacher_dashboard():
    # Add your logic here
    return render_template("teacher.html", name=session.get("name"))

@app.route('/student')
def student_dashboard():
    # Add your logic here
    return render_template("student.html", name=session.get("name"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        mobile = request.form['mobile']
        parent_mobile = request.form['parent_mobile']
        password = request.form['passwords']  # match the form field name
        photo = request.files['photo']

        # Save photo
        filename = None
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join('static/images', filename))

        # Insert into database
        new_student = Student(
            name=name,
            department=department,
            email=email,
            mobile=mobile,
            parent_mobile=parent_mobile,
            password=password,
            photo=filename
        )

        db.session.add(new_student)
        db.session.commit()
        flash("Registration successful! You can login now.", "success")
        return redirect(url_for('login'))
    return render_template('registration.html')

if __name__ == "__main__":
    app.run(debug=True)
