from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash("Login successful!", "success")
            if user.role == "teacher":
                return redirect(url_for("teacher.dashboard"))
            elif user.role == "student":
                return redirect(url_for("student.dashboard"))
            elif user.role == "admin":
                return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for("auth.login"))

    return render_template("registration.html")
