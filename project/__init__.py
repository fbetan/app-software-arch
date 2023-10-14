from flask import Flask
from project.database_model import db


def create_app(database_uri='sqlite:////home/francisco/Desktop/web_app_project/project/politicians.db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)

    return app