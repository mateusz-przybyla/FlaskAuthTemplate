def test_protected_with_access_token(client):
    payload = {"email": "test@example.com", "password": "secret123"}

    client.post("/register", json=payload)
    tokens = client.post("/login", json=payload).get_json()
    access_token = tokens['access_token']

    # call protected endpoint
    response = client.get("/protected", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.get_json()['message'] == "This is a protected endpoint."

def test_protected_without_token(client):
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.get_json()['error'] == "authorization_required"