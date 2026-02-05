def test_get_bookings_unauthorized(client):
    # Should fail without a JWT token
    response = client.get("/api/bookings/")
    assert response.status_code == 401
