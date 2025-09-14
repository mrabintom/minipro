from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/')
def dashboard():
    return render_template('accounts/admin.html')

# Add more admin routes as needed
