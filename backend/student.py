from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.models import db, Student, Attendance
import os
from werkzeug.utils import secure_filename
from datetime import date, datetime

student_bp = Blueprint("student", __name__)

# --- Student Dashboard ---
@student_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "student":
        return redirect(url_for("auth.index") + "#login")
    student_id = session["user_id"]

    attendance_records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()

    # Exclude Saturdays (5) and Sundays (6)
    working_days = [r for r in attendance_records if r.date.weekday() not in (5, 6)]
    total_days = len(working_days)
    present_days = sum(1 for r in working_days if r.time)

    attendance_percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0

    return render_template(
        "student.html",
        attendance_records=attendance_records,
        attendance_percentage=attendance_percentage,
        name=session.get("name")
    )

# --- Student Registration ---
@student_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        department = request.form.get("department")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        parent_mobile = request.form.get("parent_mobile")
        password = request.form.get("password")   # ✅ field name fixed

        # Save photo if uploaded
        photo = request.files.get("photo")
        filename = None
        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo_path = os.path.join("static/images", filename)
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
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.index") + "#login")  # back to login
        except Exception as e:
            db.session.rollback()
            flash("Error: " + str(e), "danger")
            return redirect(url_for("student.register"))

    return render_template("registration.html")

# --- Student Login ---
@student_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    student = Student.query.filter_by(email=email, password=password).first()
    if student:
        session["user_id"] = student.student_id
        session["role"] = "student"
        session["name"] = student.name
        flash("Welcome " + student.name, "success")
        return redirect(url_for("student.dashboard"))
    else:
        flash("Invalid email or password", "danger")
        return redirect(url_for("auth.index") + "#login")

# --- Student Logout ---
@student_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.index"))
