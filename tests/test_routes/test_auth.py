def test_register_endpoint(client):
    payload = {
        "username": "alvin_test",
        "email": "alvin@test.com",
        "password": "password123",
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    assert "success" in response.get_json()["status"]


def test_login_invalid_user(client):
    response = client.post(
        "/api/auth/login", json={"email": "none@test.com", "password": "123"}
    )
    assert response.status_code == 401
