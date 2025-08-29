from flask import Flask, jsonify

from app.config import Config
from app.extensions import api, jwt, db, migrate

from app.resources.test import blp as TestBlueprint
from app.resources.user import blp as UserBlueprint

from blocklist import BLOCKLIST

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has been revoked.", "error": "token_revoked"}), 401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"message": "Request does not contain an access token.", "error": "authorization_required"}), 401)
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token is not fresh.", "error": "fresh_token_required"}), 401)

    api.register_blueprint(TestBlueprint)
    api.register_blueprint(UserBlueprint)

    return app