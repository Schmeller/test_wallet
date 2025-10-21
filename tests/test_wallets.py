import uuid
import pytest

def test_create_wallet(client):
    response = client.post("/api/v1/wallets")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["balance"] == 0.0

def test_get_wallet_not_found(client):
    wallet_id = uuid.uuid4()
    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 404

def test_deposit_operation(client):
    wallet_response = client.post("/api/v1/wallets")
    wallet_id = wallet_response.json()["id"]

    operation_data = {
        "operation_type": "DEPOSIT",
        "amount": 1000.0
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    print("RESPONSE:", response.json())
    assert response.status_code == 200
    assert response.json()["balance"] == 1000.0

    response = client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.json()["balance"] == 1000.0

def test_withdraw_operation(client):
    wallet_response = client.post("/api/v1/wallets")
    wallet_id = wallet_response.json()["id"]

    client.post(f"/api/v1/wallets/{wallet_id}/operation", json={
        "operation_type": "DEPOSIT",
        "amount": 1000.0
    })

    operation_data = {
        "operation_type": "WITHDRAW",
        "amount": 500.0
    }
    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 200
    assert response.json()["balance"] == 500.0

def test_insufficient_funds(client):
    wallet_response = client.post("/api/v1/wallets")
    wallet_id = wallet_response.json()["id"]

    client.post(f"/api/v1/wallets/{wallet_id}/operation", json={
        "operation_type": "DEPOSIT",
        "amount": 100.0
    })
    
    operation_data = {
        "operation_type": "WITHDRAW",
        "amount": 500.0
    }

    response = client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]
