import pytest
import random
import string
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

init_db()
client = TestClient(app)

def random_owner_name():
    return ''.join(random.choices(string.ascii_letters, k=8))

@pytest.fixture()
def create_account1():
    name = random_owner_name()
    pin = "1234"
    balance = 1000.0
    response = client.post("/accounts/", json={"owner": name, "pin": pin, "balance": balance})
    data = response.json()
    yield {"id": data['id'], "pin": pin, "name": name, "balance": balance}
    client.delete(f"/accounts/delete/{data['id']}?pin={pin}")

@pytest.fixture()
def create_account2():
    name = random_owner_name()
    pin = "4321"
    balance = 1000.0
    response = client.post("/accounts/", json={"owner": name, "pin": pin, "balance": balance})
    data = response.json()
    yield {"id": data['id'], "pin": pin, "name": name, "balance": balance}
    client.delete(f"/accounts/delete/{data['id']}?pin={pin}")