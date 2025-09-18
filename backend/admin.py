from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))
    return render_template("admin.html")
