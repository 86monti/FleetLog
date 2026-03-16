from fastapi.testclient import TestClient


def test_create_vehicle(client: TestClient, auth_headers: dict, vehicle_payload: dict):
    response = client.post(
        "/api/v1/vehicles/",
        json=vehicle_payload,
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()

    assert data["make"] == vehicle_payload["make"]
    assert data["model"] == vehicle_payload["model"]
    assert data["year"] == vehicle_payload["year"]
    assert data["current_odometer"] == vehicle_payload["current_odometer"]
    assert "id" in data
    assert "owner_id" in data


def test_list_vehicles(client: TestClient, auth_headers: dict, created_vehicle: dict):
    response = client.get("/api/v1/vehicles/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == created_vehicle["id"]


def test_get_vehicle(client: TestClient, auth_headers: dict, created_vehicle: dict):
    vehicle_id = created_vehicle["id"]

    response = client.get(f"/api/v1/vehicles/{vehicle_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == vehicle_id
    assert data["make"] == created_vehicle["make"]


def test_update_vehicle(client: TestClient, auth_headers: dict, created_vehicle: dict):
    vehicle_id = created_vehicle["id"]

    updated_payload = {
        "make": "Mazda",
        "model": "MX-5 NC2",
        "year": 2010,
        "registration_plate": "XYZ999",
        "vin": "JM0UPDATED123456789",
        "current_odometer": 211500,
    }

    response = client.put(
        f"/api/v1/vehicles/{vehicle_id}",
        json=updated_payload,
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["registration_plate"] == "XYZ999"
    assert data["current_odometer"] == 211500


def test_delete_vehicle(client: TestClient, auth_headers: dict, created_vehicle: dict):
    vehicle_id = created_vehicle["id"]

    delete_response = client.delete(
        f"/api/v1/vehicles/{vehicle_id}",
        headers=auth_headers,
    )
    get_response = client.get(f"/api/v1/vehicles/{vehicle_id}", headers=auth_headers)

    assert delete_response.status_code == 204
    assert get_response.status_code == 404