from flask import Blueprint, render_template


information_bp = Blueprint('information', __name__)


@information_bp.get('/covid/information')
def information_local():
    map_TF = False
    return render_template('_pages/covid/local.html', map_TF=map_TF)


@information_bp.get('/covid/information/global')
def information_global():
    map_TF = False
    return render_template('_pages/covid/global.html', map_TF=map_TF)

