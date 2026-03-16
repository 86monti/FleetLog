from fastapi.testclient import TestClient


def test_create_user(client: TestClient, user_payload: dict):
    response = client.post("/api/v1/users/", json=user_payload)

    assert response.status_code == 201
    data = response.json()

    assert data["email"] == user_payload["email"]
    assert data["full_name"] == user_payload["full_name"]
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_duplicate_email(client: TestClient, user_payload: dict):
    first_response = client.post("/api/v1/users/", json=user_payload)
    second_response = client.post("/api/v1/users/", json=user_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "email already registered"


def test_login_success(client: TestClient, created_user: dict, user_payload: dict):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user_payload["email"],
            "password": user_payload["password"],
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client: TestClient, created_user: dict, user_payload: dict):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user_payload["email"],
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"


def test_get_current_user(client: TestClient, auth_headers: dict, user_payload: dict):
    response = client.get("/api/v1/users/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == user_payload["email"]
    assert data["full_name"] == user_payload["full_name"]


def test_get_current_user_unauthorized(client: TestClient):
    response = client.get("/api/v1/users/me")

    assert response.status_code in [401, 403]