from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.models import db, Teacher

teacher_bp = Blueprint("teacher", __name__)

@teacher_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        teacher = Teacher.query.filter_by(email=email, password=password).first()
        if teacher:
            session["user_id"] = teacher.teacher_id
            session["role"] = "teacher"
            session["name"] = teacher.name
            flash("Welcome, " + teacher.name, "success")
            return redirect(url_for("teacher.dashboard"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.index") + "#login")
    return render_template("teacher_login.html")

@teacher_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "teacher":
        return redirect(url_for("auth.index") + "#login")
    return render_template("teacher.html")
