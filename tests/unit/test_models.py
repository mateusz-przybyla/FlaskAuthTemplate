from app.models import UserModel

def test_user_model_fiels():
    user = UserModel(email="a@b.com", password="secret")
    assert user.email == "a@b.com"
    assert user.password == "secret"