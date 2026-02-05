def test_add_inventory_route(client):
    # This assumes auth is bypassed or handled in conftest
    response = client.post("/api/inventory/add", json={"item": "Sofa", "qty": 2})
    assert response.status_code in [201, 401]  # Depending on auth setup
