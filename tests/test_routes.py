from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
import random
import string
import pytest

init_db()

client = TestClient(app)

def random_owner_name():
    return ''.join(random.choices(string.ascii_letters, k=8))

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
    

@pytest.fixture()
def create_account():
    name = random_owner_name()
    pin = "1234"
    balance = 1000.0
    
    response = client.post("/accounts/", json={
        "owner": name,
        "pin": pin,
        "balance": balance
    })
    
    data = response.json()
    account_id = data['id']
    
    yield {"id": account_id, "pin": pin, "name": name, "balance": balance}

    client.delete(f"/accounts/delete/{account_id}?pin={pin}")
    

def test_get_account_by_id(create_account):
    response = client.get(f"/accounts/{create_account['id']}?pin={create_account['pin']}")
    assert response.status_code == 200
    data = response.json()
    assert data['owner'] == create_account['name']
    assert data['balance'] == create_account['balance']

@pytest.mark.parametrize("get_url, expected_status, expected_detail", [
    (lambda acc: f"/accounts/{acc['id']}?pin=0000", 400, "Неверный PIN-код"),
    (lambda acc: f"/accounts/999999?pin=1234", 400, "Аккаунт с таким ID не найден"),
    (lambda acc: f"/accounts/{acc['id']}", 422, None),
])
def test_get_account_by_id_negative(create_account, get_url, expected_status, expected_detail):
    response = client.get(get_url(create_account))
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()["detail"] == expected_detail
        

def test_deposit(create_account):
    response = client.post(f"/accounts/{create_account['id']}/deposit", json={
        "amount": 1000.0,
        "pin": create_account['pin']
    })
    assert response.status_code == 200
    data = response.json()
    assert data['balance'] == create_account['balance'] + 1000.0
    
