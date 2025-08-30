from flask import Flask

from app.config import Config
from app.extensions import api, jwt, db, migrate

from app.resources.test import blp as TestBlueprint
from app.resources.user import blp as UserBlueprint

from app import jwt_callbacks

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api.init_app(app)
    jwt.init_app(app)

    api.register_blueprint(TestBlueprint)
    api.register_blueprint(UserBlueprint)

    return app