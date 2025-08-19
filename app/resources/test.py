from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("test", __name__, description="Test operations")

@blp.route("/test")
class Test(MethodView):
    def get(self):
        return {"msg": "This is a test endpoint"}
