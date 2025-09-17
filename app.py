from flask import Flask, render_template, request, redirect, url_for, session, flash
from backend.models import db, Admin, Teacher, Student, Attendance, Fine
import os
from werkzeug.utils import secure_filename
import psycopg2

app = Flask(__name__)
app.secret_key = "supersecret"
app.config.from_object("config.Config")
app.secret_key = "your-secret-key"  # Replace with a secure key

# Set config directly
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin%40123@localhost:5432/minipro"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

with app.app_context():
    db.create_all()

# psycopg2 connection (keep this at the top, after Flask app setup)
conn = psycopg2.connect(
    host="localhost",
    dbname="minipro",
    user="postgres",
    password="Admin@123"
)

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
    return render_template('admin.html')

@app.route('/teacher')
def teacher_dashboard():
    return render_template('teacher.html')

@app.route('/student')
def student_dashboard():
    return render_template('student.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        mobile = request.form['mobile']
        parent_mobile = request.form['parent_mobile']
        password = request.form['passwords']  # matches form input name
        photo = request.files['photo']

        filename = None
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join('static/images', filename)
            photo.save(photo_path)

        new_student = Student(
            name=name,
            department=department,
            email=email,
            mobile=mobile,
            parent_mobile=parent_mobile,
            password=password,
            photo=filename
        )

        try:
            db.session.add(new_student)
            db.session.commit()
            flash("Registration successful! You can log in now.", "success")
            return redirect(url_for('index') + "#login")

        except Exception as e:
            db.session.rollback()
            flash("Error: " + str(e), "danger")
            return redirect(url_for('register'))

    return render_template('registration.html')

@app.route('/login_psycopg', methods=['POST'])
def login_psycopg():
    email = request.form['email']
    password = request.form['password']

    cur = conn.cursor()

    # 1. Check students
    cur.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
    student = cur.fetchone()
    if student:
        cur.close()
        return redirect(url_for('student_dashboard'))

    # 2. Check teachers
    cur.execute("SELECT * FROM teachers WHERE email=%s AND password=%s", (email, password))
    teacher = cur.fetchone()
    if teacher:
        cur.close()
        return redirect(url_for('teacher_dashboard'))

    # 3. Check admins
    cur.execute("SELECT * FROM admins WHERE email=%s AND password=%s", (email, password))
    admin = cur.fetchone()
    if admin:
        cur.close()
        return redirect(url_for('admin_dashboard'))

    cur.close()

    # If not found anywhere
    flash("Invalid email or password", "danger")
    return redirect(url_for('index') + "#login")

if __name__ == "__main__":
    app.run(debug=True)
