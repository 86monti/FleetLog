import os
import sys
from collections.abc import Generator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PROJECT_NAME"] = "FleetLog Test API"
os.environ["VERSION"] = "0.1.0"
os.environ["DEBUG"] = "False"
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def user_payload():
    return {
        "email": "danny@example.com",
        "password": "testpassword123",
        "full_name": "Danny Hedayati",
    }


@pytest.fixture
def created_user(client: TestClient, user_payload: dict):
    response = client.post("/api/v1/users/", json=user_payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_token(client: TestClient, created_user: dict, user_payload: dict) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user_payload["email"],
            "password": user_payload["password"],
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def vehicle_payload():
    return {
        "make": "Mazda",
        "model": "MX-5 NC2",
        "year": 2010,
        "registration_plate": "ABC123",
        "vin": "JM0TEST1234567890",
        "current_odometer": 210000,
    }


@pytest.fixture
def created_vehicle(client: TestClient, auth_headers: dict, vehicle_payload: dict):
    response = client.post(
        "/api/v1/vehicles/",
        json=vehicle_payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()