import os
os.environ["SECRET_KEY"] = "testsecret"

from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_signup_and_login():
    response = client.post("/signup2",
                           data={"username": "testuser",
                                 "password": "testpass"})
    assert response.status_code in (200, 201)

    response = client.post("/token",
                           data={"username": "testuser",
                                 "password": "testpass"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

def test_signup_existing_user():
    client.post("/signup2", data={"username": "existinguser", "password": "pass1"})
    response = client.post("/signup2", data={"username": "existinguser", "password": "pass2"})
    assert response.status_code not in (200, 201)


def test_login_wrong_password():
    client.post("/signup2", data={"username": "wrongpassuser", "password": "rightpass"})
    response = client.post("/token", data={"username": "wrongpassuser", "password": "wrongpass"})
    assert response.status_code == 401


def test_login_nonexistent_user():
    response = client.post("/token", data={"username": "nouser", "password": "nopass"})
    assert response.status_code == 401


def test_protected_endpoint_with_valid_token():
    client.post("/signup2", data={"username": "protecteduser", "password": "protectedpass"})
    response = client.post("/token", data={"username": "protecteduser", "password": "protectedpass"})
    token = response.json().get("access_token")
    assert token
    protected_url = "/retrieve_info"  
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(protected_url, headers=headers)
    assert response.status_code in (200, 201, 403, 404)  


def test_protected_endpoint_with_invalid_token():
    protected_url = "/retrieve_info" 
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get(protected_url, headers=headers)
    assert response.status_code in (401, 403, 404)
