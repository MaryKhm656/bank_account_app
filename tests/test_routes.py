from conftest import random_owner_name
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_create_account():
    owner = random_owner_name()
    pin = "1234"
    balance = 1000.0
    
    response = client.post("/accounts/", json={
        "owner": owner,
        "pin": pin,
        "balance": balance
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["owner"] == owner
    assert data["balance"] == balance
    account_id = data['id']
    
    client.delete(f"/accounts/delete/{account_id}?pin={pin}")

@pytest.mark.parametrize("payload, expected_status, expected_detail", [
    ({"pin": "1234", "balance": 1000.0}, 422, None),
    ({"owner": "placeholder", "balance": 1000.0}, 422, None),
    ({"owner": "placeholder", "pin": "12", "balance": 1000.0}, 400, "PIN должен быть 4 или более символов"),
    ({"owner": "placeholder", "pin": "1234", "balance": -100.0}, 400, "Начальный баланс не может быть отрицательным"),
    ({"owner": "", "pin": "1234", "balance": 100.0}, 400, "Имя владельца не может быть пустым"),
])
def test_create_account_invalid(payload, expected_status, expected_detail):
    if payload.get("owner") == "placeholder":
        payload["owner"] = random_owner_name()

    response = client.post("/accounts/", json=payload)
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()["detail"] == expected_detail
    

def test_get_account_by_id(create_account1):
    response = client.get(f"/accounts/{create_account1['id']}?pin={create_account1['pin']}")
    assert response.status_code == 200
    data = response.json()
    assert data['owner'] == create_account1['name']
    assert data['balance'] == create_account1['balance']

@pytest.mark.parametrize("get_url, expected_status, expected_detail", [
    (lambda acc: f"/accounts/{acc['id']}?pin=0000", 400, "Неверный PIN-код"),
    (lambda acc: f"/accounts/999999?pin=1234", 400, "Аккаунт с таким ID не найден"),
    (lambda acc: f"/accounts/{acc['id']}", 422, None),
])
def test_get_account_by_id_negative(create_account1, get_url, expected_status, expected_detail):
    response = client.get(get_url(create_account1))
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()["detail"] == expected_detail
        

def test_deposit(create_account1):
    response = client.post(f"/accounts/{create_account1['id']}/deposit", json={
        "amount": 1000.0,
        "pin": create_account1['pin']
    })
    assert response.status_code == 200
    data = response.json()
    assert data['balance'] == create_account1['balance'] + 1000.0
    
@pytest.mark.parametrize("payload, expected_status, expected_detail", [
    ({"amount": 1000.0, "pin": 1234}, 422, None),
    ({"amount": "abc", "pin": "1234"}, 422, None),
    ({}, 422, None),
    ({"amount": None, "pin": "1234"}, 422, None),
    ({"amount": 1000.0, "pin": "0000"}, 400, "Неверный PIN-код"),
    ({"amount": -1000.0, "pin": "1234"}, 400, "Сумма должна быть положительной")
])
def test_deposit_invalid(create_account1, payload, expected_status, expected_detail):
    response = client.post(f"/accounts/{create_account1['id']}/deposit", json=payload)
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()['detail'] == expected_detail
        
def test_deposit_nonexistent_account():
    response = client.post("/accounts/99999/deposit", json={
        "amount": 1000.0,
        "pin": "1234"
    })
    assert response.status_code == 400
    assert response.json()['detail'] == "Аккаунт с таким ID не найден"


def test_withdraw(create_account1):
    response = client.post(f"/accounts/{create_account1['id']}/withdraw", json={
        "amount": 100.0,
        "pin": create_account1['pin']
    })
    assert response.status_code == 200
    data = response.json()
    assert data['balance'] == create_account1['balance'] - 100.0

@pytest.mark.parametrize("payload, expected_status, expected_detail", [
    ({"amount": 1000.0, "pin": 1234}, 422, None),
    ({"amount": "abc", "pin": "1234"}, 422, None),
    ({}, 422, None),
    ({"amount": None, "pin": "1234"}, 422, None),
    ({"amount": 1000.0, "pin": "0000"}, 400, "Неверный PIN-код"),
    ({"amount": -1000.0, "pin": "1234"}, 400, "Сумма должна быть положительной")
])
def test_withdraw_invalid(create_account1, payload, expected_status, expected_detail):
    response = client.post(f"accounts/{create_account1['id']}/withdraw", json=payload)
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()['detail'] == expected_detail

def test_withdraw_nonexistent_account():
    response = client.post("/accounts/99999/withdraw", json={
        "amount": 1000.0,
        "pin": "1234"
    })
    assert response.status_code == 400
    assert response.json()['detail'] == "Аккаунт с таким ID не найден"
    
    
def test_transfer(create_account1, create_account2):
    response = client.post(f"/accounts/{create_account1['id']}/{create_account2['id']}/transfer", json={
        "amount": 500.0,
        "pin": create_account1['pin']
    })
    assert response.status_code == 200
    data1, data2 = response.json()
    assert data1['balance'] == create_account1['balance'] - 500.0
    assert data2['balance'] == create_account2['balance'] + 500.0

@pytest.mark.parametrize("payload, expected_status, expected_detail", [
    ({"amount": 1000.0, "pin": 1234}, 422, None),
    ({"amount": "abc", "pin": "1234"}, 422, None),
    ({}, 422, None),
    ({"amount": None, "pin": "1234"}, 422, None),
    ({"amount": 1000.0, "pin": "0000"}, 400, "Неверный PIN-код"),
    ({"amount": -1000.0, "pin": "1234"}, 400, "Сумма должна быть положительной")
])
def test_transfer_invalid(create_account1, create_account2, payload, expected_status, expected_detail):
    response = client.post(f"accounts/{create_account1['id']}/{create_account2['id']}/transfer", json=payload)
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()['detail'] == expected_detail
        
def test_transfer_nonexistent_to_account(create_account2):
    response = client.post(f"/accounts/99999/{create_account2['id']}/transfer", json={
        "amount": 500.0,
        "pin": "1234"
    })
    assert response.status_code == 400
    assert response.json()['detail'] == "Аккаунт с ID 99999 не найден"

def test_transfer_nonexistent_from_account(create_account1):
    response = client.post(f"/accounts/{create_account1['id']}/99999/transfer", json={
        "amount": 500.0,
        "pin": "1234"
    })
    assert response.status_code == 400
    assert response.json()['detail'] == "Аккаунт с ID 99999 не найден"
    
    
def test_delete(create_account1):
    account_id = create_account1['id']
    response = client.get(f"/accounts/{account_id}?pin={create_account1['pin']}")
    assert response.status_code == 200
    response = client.delete(f"accounts/delete/{account_id}?pin={create_account1['pin']}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Аккаунт {account_id} успешно удалён"}
    response = client.get(f"/accounts/{account_id}?pin={create_account1['pin']}")
    assert response.status_code == 400
    assert response.json()['detail'] == "Аккаунт с таким ID не найден"
    
def test_delete_invalid_pin(create_account1):
    response = client.delete(f"/accounts/delete/{create_account1['id']}?pin=1545214")
    assert response.status_code == 400
    assert response.json()['detail'] == "Неверный PIN-код"
    
def test_delete_nonexistent_account():
    response = client.delete("/accounts/delete/412584?pin=1234")
    assert response.status_code == 400
    assert response.json()['detail'] == "Аккаунт с таким ID не найден"