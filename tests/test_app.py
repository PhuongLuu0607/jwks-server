import pytest
from fastapi.testclient import TestClient
from main import app

# Create a test client for FastAPI
client = TestClient(app)


def test_jwks_endpoint_returns_keys():
    """JWKS endpoint should return at least one active key."""
    response = client.get("/.well-known/jwks.json")
    assert response.status_code == 200
    data = response.json()
    assert "keys" in data
    assert len(data["keys"]) > 0
    assert data["keys"][0]["kty"] == "RSA"


def test_auth_endpoint_returns_token():
    """Auth endpoint should return a signed JWT."""
    response = client.post("/auth")
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)


def test_auth_expired_token():
    """Auth endpoint with expired=true should still return a token."""
    response = client.post("/auth?expired=true")
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
