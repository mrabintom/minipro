from flask import Flask, render_template, redirect, url_for, session
from backend.models import db
from backend.auth import auth_bp
from backend.student import student_bp
from backend.teacher import teacher_bp
from backend.admin import admin_bp
from flask import Blueprint


app = Flask(__name__)
app.secret_key = "your-secret-key"  # ⚠️ Replace with a secure random key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin%40123@localhost:5432/minipro"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(teacher_bp, url_prefix="/teacher")
app.register_blueprint(admin_bp, url_prefix="/admin")

# Default route → show index.html
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index")
def index_redirect():
    return redirect(url_for("auth.index"))


@app.route("/student/dashboard")
def student_dashboard():
    if "user_id" not in session or session.get("role") != "student":
        return redirect(url_for("auth.index") + "#login")
    return render_template("student.html")

@app.route("/teacher/dashboard")
def teacher_dashboard():
    if "user_id" not in session or session.get("role") != "teacher":
        return redirect(url_for("auth.index") + "#login")
    return render_template("teacher.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.index") + "#login")
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
