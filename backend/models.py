from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    password = db.Column(db.Text, nullable=False)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(50))
    password = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False)

class Student(db.Model):
    __tablename__ = "students"   # 👈 important, ensure this matches your real table name
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    parent_mobile = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255))

class Attendance(db.Model):
    __tablename__ = "attendance"
    attendance_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))  # ✅ correct reference
    student_name = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

class Fine(db.Model):
    __tablename__ = 'fine'
    fine_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete="CASCADE"))
    date = db.Column(db.Date, nullable=False)
    late_by = db.Column(db.Integer)
    amount = db.Column(db.Numeric(10,2))
    status = db.Column(db.String(10), default='Unpaid')
    parent_notified = db.Column(db.Boolean, default=False)
