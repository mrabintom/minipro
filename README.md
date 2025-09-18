# Smart Attendance & Fine Management System

A web-based application for managing student attendance, fines, and dashboards for students, teachers, and admins. Built with Flask, SQLAlchemy, and Bootstrap.

---

## Features

- **Student, Teacher, and Admin Login**
- **Student Registration with Photo Upload**
- **Role-based Dashboards**
- **Attendance Tracking and Visualization**
- **Fine Management and Payment Status**
- **Session-based Authentication**
- **Responsive UI with Bootstrap**

---

## Project Structure

```
attendance/
│
├── app.py                  # Main Flask app, blueprint registration
├── backend/
│   ├── __init__.py
│   ├── models.py           # SQLAlchemy models (Student, Teacher, Admin, Attendance, Fine)
│   ├── auth.py             # Auth routes (login/logout)
│   ├── student.py          # Student routes (dashboard, registration)
│   ├── teacher.py          # Teacher routes (dashboard)
│   └── admin.py            # Admin routes (dashboard)
│
├── templates/
│   ├── index.html          # Landing/login page
│   ├── registration.html   # Student registration page
│   ├── student.html        # Student dashboard
│   ├── teacher.html        # Teacher dashboard
│   └── admin.html          # Admin dashboard
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── .venv/                  # Python virtual environment
└── git                     # Git helper commands
```

---
