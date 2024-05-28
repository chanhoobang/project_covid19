from flask import Blueprint, render_template


home_bp = Blueprint('home', __name__)


@home_bp.get('/')
def public_home():
    return render_template('_pages/default.html')
