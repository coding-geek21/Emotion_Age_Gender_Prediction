from flask import Flask
from os import path

IMG_FOLDER = path.join('static', 'img-uploads')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "9dcaa8494e292cce38fa42394"
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
