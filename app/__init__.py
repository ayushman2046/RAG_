from flask import Flask
from app import config
from app.main.model import Database


def create_app(ENV):
    app = Flask(__name__)
    app.config.from_object(config.config_by_name[ENV])
    app.db = Database(app)
    
    return app