import pytest
from faker import Faker

fake = Faker()


def test_register_endpoint(client):
    """Test registration with random user data."""
    payload = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "SecurePassword123!",
    }
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 201
    assert response.get_json()["status"] == "success"


def test_login_scenario(client, app):
    """Test registration followed by a successful login."""
    email = fake.email()
    password = "testpassword123"

    # First, create the user
    client.post(
        "/api/auth/register",
        json={"username": fake.user_name(), "email": email, "password": password},
    )

    # Then, attempt login
    login_response = client.post(
        "/api/auth/login", json={"email": email, "password": password}
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.get_json()["data"]
