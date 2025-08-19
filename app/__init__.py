from flask import Flask

from app.config import Config
from app.extensions import api, jwt

from app.resources.test import blp as TestBlueprint

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    api.init_app(app)
    jwt.init_app(app)

    api.register_blueprint(TestBlueprint)

    return app