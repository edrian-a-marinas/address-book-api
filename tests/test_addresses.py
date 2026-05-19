import pytest


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_address_success(client, sample_address):
    response = client.post("/api/v1/addresses/", json=sample_address)
    assert response.status_code == 201
    data = response.json()
    assert data["street"] == sample_address["street"]
    assert data["city"] == sample_address["city"]
    assert data["latitude"] == sample_address["latitude"]
    assert "id" in data


def test_create_address_missing_required_field(client):
    response = client.post("/api/v1/addresses/", json={"street": "123 Main St"})
    assert response.status_code == 422


def test_create_address_invalid_latitude(client, sample_address):
    payload = {**sample_address, "latitude": 999}
    response = client.post("/api/v1/addresses/", json=payload)
    assert response.status_code == 422


def test_create_address_invalid_longitude(client, sample_address):
    payload = {**sample_address, "longitude": -999}
    response = client.post("/api/v1/addresses/", json=payload)
    assert response.status_code == 422


def test_create_address_empty_street(client, sample_address):
    payload = {**sample_address, "street": "   "}
    response = client.post("/api/v1/addresses/", json=payload)
    assert response.status_code == 422


# ── READ ──────────────────────────────────────────────────────────────────────

def test_get_address_success(client, sample_address):
    created = client.post("/api/v1/addresses/", json=sample_address).json()
    response = client.get(f"/api/v1/addresses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_address_not_found(client):
    response = client.get("/api/v1/addresses/9999")
    assert response.status_code == 404


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_address_success(client, sample_address):
    created = client.post("/api/v1/addresses/", json=sample_address).json()
    response = client.put(f"/api/v1/addresses/{created['id']}", json={"city": "Makati"})
    assert response.status_code == 200
    assert response.json()["city"] == "Makati"


def test_update_address_not_found(client):
    response = client.put("/api/v1/addresses/9999", json={"city": "Makati"})
    assert response.status_code == 404


def test_update_address_invalid_latitude(client, sample_address):
    created = client.post("/api/v1/addresses/", json=sample_address).json()
    response = client.put(f"/api/v1/addresses/{created['id']}", json={"latitude": 999})
    assert response.status_code == 422


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_address_success(client, sample_address):
    created = client.post("/api/v1/addresses/", json=sample_address).json()
    response = client.delete(f"/api/v1/addresses/{created['id']}")
    assert response.status_code == 204


def test_delete_address_not_found(client):
    response = client.delete("/api/v1/addresses/9999")
    assert response.status_code == 404


def test_delete_address_no_longer_accessible(client, sample_address):
    created = client.post("/api/v1/addresses/", json=sample_address).json()
    client.delete(f"/api/v1/addresses/{created['id']}")
    response = client.get(f"/api/v1/addresses/{created['id']}")
    assert response.status_code == 404


# ── NEARBY ────────────────────────────────────────────────────────────────────

def test_nearby_returns_address_within_distance(client, sample_address):
    client.post("/api/v1/addresses/", json=sample_address)
    response = client.get("/api/v1/addresses/nearby", params={
        "latitude": 14.5995,
        "longitude": 120.9842,
        "distance_km": 10
    })
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_nearby_excludes_address_outside_distance(client, sample_address):
    client.post("/api/v1/addresses/", json=sample_address)
    # Tokyo coordinates — far from Quezon City
    response = client.get("/api/v1/addresses/nearby", params={
        "latitude": 35.6762,
        "longitude": 139.6503,
        "distance_km": 10
    })
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_nearby_missing_params(client):
    response = client.get("/api/v1/addresses/nearby")
    assert response.status_code == 422