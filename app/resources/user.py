from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import UserModel
from app.schemas import UserSchema

blp = Blueprint("user", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            email=user_data['email'],
            password=sha256.hash(user_data['password'])
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the user.")

        return {"message": "User created successfully."}, 201
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the user.")

        return {"message": "User deleted."}, 200
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user and sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")