from flask import Blueprint, render_template


information_bp = Blueprint('information', __name__)


@information_bp.get('/covid/information')
def information_local():
    return render_template('_pages/covid/local.html')


@information_bp.get('/covid/information/global')
def information_global():
    return render_template('_pages/covid/global.html')

