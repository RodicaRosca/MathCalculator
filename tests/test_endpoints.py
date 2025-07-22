from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_signup_and_login():
    response = client.post("/signup", data={"username": "testuser", "password": "testpass"})
    assert response.status_code in (200, 201)

    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token
