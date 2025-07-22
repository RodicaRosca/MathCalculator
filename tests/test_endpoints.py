from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def login_new_user():
    username = "testuser"
    password = "testpass"
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token

def login_wrong_password():
    username = "testuser"
    response_bad = client.post("/token", data={"username": username, "password": "wrong"})
    assert response_bad.status_code == 401

def signup_2_times():
    username = "testuser"
    password = "testpass"
    response = client.post("/signup2", data={"username": username, "password": password})
    assert response.status_code in (200, 201)

    # Try to signup again with the same username
    response_dup = client.post("/signup2", data={"username": username, "password": password})
    assert response_dup.status_code == 400

def test_signup_and_login_and_protected():
    # Signup a new user
    token = "supertestsecret"
    username = "testuser"
    password = "testpass"
    response = client.post("/signup2", data={"username": username, "password": password})
    assert response.status_code in (200, 201)

    # Try to signup again (should fail)
    response_dup = client.post("/signup2", data={"username": username, "password": password})
    assert response_dup.status_code == 400

    # Access protected endpoint with token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert "user" in response.json() or "msg" in response.json()

    # Access protected endpoint without token
    response = client.get("/protected")
    assert response.status_code == 401

def test_signup_and_login_and_protected():
    import uuid
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpass"
    response = client.post("/signup2", data={"username": username, "password": password})
    assert response.status_code in (200, 201)
    # Try to signup again (should fail)
    response_dup = client.post("/signup2", data={"username": username, "password": password})
    assert response_dup.status_code == 400

def test_signup_bad_request():
    # Missing password
    response = client.post("/signup", data={"username": "user_only"})
    assert response.status_code == 422
    
    # Missing username
    response = client.post("/signup", data={"password": "pass_only"})
    assert response.status_code == 422
