from app.models import UserModel

def test_register_user(client, db_session):
    payload = {"email": "test@example.com", "password": "secret123"}

    response = client.post("/register", json=payload)
    assert response.status_code == 201
    assert response.get_json()['message'] == "User created successfully."

    user = db_session.query(UserModel).filter_by(email="test@example.com").first()
    assert user is not None
    assert user.email == "test@example.com"

def test_register_and_login(client):
    payload = {"email": "test@example.com", "password": "secret123"}

    client.post("/register", json=payload)
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    tokens = response.get_json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

def test_register_duplicate_user(client):
    payload = {"email": "test@example.com", "password": "secret123"}

    client.post("/register", json=payload)
    response = client.post("/register", json=payload)
    assert response.status_code == 409
    assert response.get_json()['message'] == "A user with that email already exists."