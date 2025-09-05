import os
from flask import Flask
from dotenv import load_dotenv

from app.config import DevConfig, ProdConfig
from app.extensions import api, jwt, db, migrate
from app.resources.test import blp as TestBlueprint
from app.resources.user import blp as UserBlueprint
from app import jwt_callbacks

def create_app(config_class=None):
    app = Flask(__name__)
    load_dotenv()

    if config_class is None:
        config_name = os.getenv("FLASK_CONFIG", "development")
        if config_name == "production":
            config_class = ProdConfig
        elif config_name == "development":
            config_class = DevConfig

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    api.init_app(app)
    jwt.init_app(app)

    api.register_blueprint(TestBlueprint)
    api.register_blueprint(UserBlueprint)

    return app