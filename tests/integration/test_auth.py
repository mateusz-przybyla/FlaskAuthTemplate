from blocklist import BLOCKLIST

def test_logout_revokes_access_token(client):
    payload = {"email": "test@example.com", "password": "secret123"}

    client.post("/register", json=payload)
    tokens = client.post("/login", json=payload).get_json()
    access_token = tokens['access_token']

    response = client.post("/logout", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert len(BLOCKLIST) == 1

    # access protected endpoint with revoked token
    response = client.get("/protected", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401
    assert response.get_json()['error'] == "token_revoked"

def test_refresh_token_flow(client):
    payload = {"email": "test@example.com", "password": "secret123"}

    client.post("/register", json=payload)
    tokens = client.post("/login", json=payload).get_json()
    refresh_token = tokens['refresh_token']

    # refresh access token
    response = client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    new_access = response.get_json()['access_token']
    assert new_access