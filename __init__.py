from flask import Flask, Blueprint
from . import config



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from .views import covid19_view
    app.register_blueprint(covid19_view.bp)

    return app