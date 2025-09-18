from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret"
    app.config.from_object("config.Config")

    # Initialize DB
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Import and register blueprints
    from backend.auth import auth_bp
    from backend.student import student_bp
    from backend.teacher import teacher_bp
    from backend.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(teacher_bp, url_prefix="/teacher")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
