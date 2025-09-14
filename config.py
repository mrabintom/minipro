import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:yourpassword@localhost:5432/attendance_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
