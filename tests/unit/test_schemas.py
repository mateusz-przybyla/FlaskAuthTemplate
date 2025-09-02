from app.schemas import UserSchema
from app.models import UserModel

def test_user_schema_validation():
    schema = UserSchema()
    user_dict = {"email": "test@example.com", "password": "abc123"}

    # Test loading (deserialization)
    loaded = schema.load(user_dict)
    assert loaded["email"] == "test@example.com"
    assert "password" in loaded

    # Test dumping (serialization)
    user_obj = UserModel(email="test@example.com", password="abc123")
    dumped = schema.dump(user_obj)
    assert dumped["email"] == "test@example.com"
    assert "password" not in dumped