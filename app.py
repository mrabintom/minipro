from flask import Flask
from backend.auth import auth_bp
from backend.teacher import teacher_bp
from backend.student import student_bp
from backend.admin import admin_bp
from backend.models import db

app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = "your-secret-key"  # Replace with a secure key

# Initialize Database
db.init_app(app)
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(teacher_bp, url_prefix="/teacher")
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)
