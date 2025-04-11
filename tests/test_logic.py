import pytest
from app.functions import (
create_account, deposit_to_account, withdraw_from_account, transfer_money,
get_history, get_account_balance, get_account_by_id, delete_account
)
from app.models import BankAccount
from app.database import init_db
import uuid

init_db()


def random_owner_name():
    return f"user_{uuid.uuid4().hex[:8]}"

def test_create_account():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=500.0)
    assert isinstance(account, BankAccount)
    assert account.owner == owner
    assert account.balance == 500.0

    delete_account(account_id=account.id, pin="1234")

def test_create_account_empty_owner():
    with pytest.raises(ValueError) as e:
        create_account(owner="", pin="1234", initial_balance=1000.0)
    assert str(e.value) == "Имя владельца не может быть пустым"
    
@pytest.mark.parametrize(
    "pin, balance, error_message",
    [
        ("4", 500.0, "PIN должен быть 4 или более символов"),
        ("1234", -500.0, "Начальный баланс не может быть отрицательным")
    ]
)
def test_create_account_invalid_data(pin, balance, error_message):
    owner = random_owner_name()
    with pytest.raises(ValueError, match=error_message):
        create_account(owner=owner, pin=pin, initial_balance=balance)
        
        
def test_deposit():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    update_account = deposit_to_account(account_id=account.id, amount=500.0, pin="1234")
    assert update_account.balance == 1500.0
    
    delete_account(account_id=update_account.id, pin="1234")
    
@pytest.mark.parametrize(
    "amount, pin, error_message",
    [
        (500.0, "4321", "Неверный PIN-код"),
        (-100.0, "1234", "Сумма должна быть положительной"),
    ]
)
def test_deposit_invalid_data(amount, pin, error_message):
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    with pytest.raises(ValueError, match=error_message):
        deposit_to_account(account_id=account.id, amount=amount, pin=pin)
        
    delete_account(account_id=account.id, pin="1234")

def test_deposit_to_nonexistent_account():
    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        deposit_to_account(account_id=999999, amount=100.0, pin="1234")
        
        
def test_withdraw():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    update_account = withdraw_from_account(account_id=account.id, amount=500.0, pin="1234")
    assert update_account.balance == 500.0
    
    delete_account(account_id=update_account.id, pin="1234")
    
@pytest.mark.parametrize(
    "amount, pin, error_message",
    [
        (500.0, "4321", "Неверный PIN-код"),
        (-500.0, "1234", "Сумма должна быть положительной"),
        (100000.0, "1234", "Недостаточно средств")
    ]
)
def test_withdraw_invalid_data(amount, pin, error_message):
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    with pytest.raises(ValueError, match=error_message):
        withdraw_from_account(account_id=account.id, amount=amount, pin=pin)
        
    delete_account(account_id=account.id, pin="1234")

def test_withdraw_to_nonexistent_account():
    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        withdraw_from_account(account_id=999999, amount=100.0, pin="1234")
        
        
def test_transfer_money():
    owner1 = random_owner_name()
    owner2 = random_owner_name()
    account1 = create_account(owner=owner1, pin="1234", initial_balance=1000.0)
    account2 = create_account(owner=owner2, pin="4321", initial_balance=1000.0)
    update_account2, update_account1 = transfer_money(from_id=account1.id, to_id=account2.id, amount=500.0, pin="1234")
    assert update_account1.balance == 500.0
    assert update_account2.balance == 1500.0
    
    delete_account(account_id=update_account1.id, pin="1234")
    delete_account(account_id=update_account2.id, pin="4321")

@pytest.mark.parametrize(
    "amount, pin, error_message",
    [
        (500.0, "4321", "Неверный PIN-код"),
        (-500.0, "1234", "Сумма должна быть положительной"),
        (100000.0, "1234", "Недостаточно средств")
    ]
)
def test_transfer_invalid_data(amount, pin, error_message):
    owner1 =random_owner_name()
    owner2 = random_owner_name()
    account1 = create_account(owner=owner1, pin="1234", initial_balance=1000.0)
    account2 = create_account(owner=owner2, pin="4321", initial_balance=1000.0)
    with pytest.raises(ValueError, match=error_message):
        transfer_money(from_id=account1.id, to_id=account2.id, amount=amount, pin=pin)
        
    delete_account(account_id=account1.id, pin="1234")
    delete_account(account_id=account2.id, pin="4321")

def test_transfer_from_nonexistent_account():
    owner = random_owner_name()
    receiver = create_account(owner=owner, pin="1234", initial_balance=500.0)
    with pytest.raises(ValueError, match="Аккаунт с ID"):
        transfer_money(from_id=999999, to_id=receiver.id, amount=100.0, pin="1234")

    delete_account(account_id=receiver.id, pin="1234")


def test_transfer_to_nonexistent_account():
    owner = random_owner_name()
    sender = create_account(owner=owner, pin="1234", initial_balance=500.0)
    with pytest.raises(ValueError, match="Аккаунт с ID"):
        transfer_money(from_id=sender.id, to_id=999999, amount=100.0, pin="1234")

    delete_account(account_id=sender.id, pin="1234")


def test_get_history():
    owner1 = random_owner_name()
    owner2 = random_owner_name()

    account1 = create_account(owner=owner1, pin="1234", initial_balance=1000.0)
    account2 = create_account(owner=owner2, pin="4321", initial_balance=500.0)

    deposit_to_account(account_id=account1.id, amount=200.0, pin="1234")
    withdraw_from_account(account_id=account1.id, amount=100.0, pin="1234")
    transfer_money(from_id=account1.id, to_id=account2.id, amount=300.0, pin="1234")

    history = get_history(account_id=account1.id, pin="1234")

    assert isinstance(history, list)
    assert len(history) >= 3 

    types = [op[0].lower() for op in history]

    assert any("пополнение" in t for t in types)
    assert any("снятие" in t for t in types)
    assert any("перевод на аккаунт" in t for t in types)

    delete_account(account_id=account1.id, pin="1234")
    delete_account(account_id=account2.id, pin="4321")

def test_get_history_wrong_pin():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=100.0)

    with pytest.raises(ValueError, match="Неверный PIN-код"):
        get_history(account_id=account.id, pin="0000")

    delete_account(account_id=account.id, pin="1234")

def test_get_history_to_nonexistent_account():
    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        get_history(account_id=999999, pin="1234")
    
def test_get_account_balance():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    balance = get_account_balance(account_id=account.id, pin="1234")
    assert balance == 1000.0
    
    delete_account(account_id=account.id, pin="1234")
    
def test_get_balance_wrong_pin():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    
    with pytest.raises(ValueError, match="Неверный PIN-код"):
        get_account_balance(account_id=account.id, pin="4321")
        
    delete_account(account_id=account.id, pin="1234")

def test_get_balance_to_nonexistent_account():
    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        get_account_balance(account_id=999999, pin="1234")
        

def test_get_account_by_id():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    account_inform = get_account_by_id(account_id=account.id, pin="1234")
    assert account_inform.id == account.id
    assert account_inform.owner == owner
    assert account_inform.balance == account.balance
    
    delete_account(account_id=account_inform.id, pin="1234")
    
def test_get_account_wrong_pin():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=1000.0)
    
    with pytest.raises(ValueError, match="Неверный PIN-код"):
        get_account_by_id(account_id=account.id, pin="4321")
        
    delete_account(account_id=account.id, pin="1234")

def test_get_account_to_nonexistent_account():
    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        get_account_by_id(account_id=999999, pin="1234")


def test_delete_account():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=100.0)

    delete_account(account_id=account.id, pin="1234")

    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        get_account_by_id(account_id=account.id, pin="1234")

def test_delete_account_wrong_pin():
    owner = random_owner_name()
    account = create_account(owner=owner, pin="1234", initial_balance=100.0)

    with pytest.raises(ValueError, match="Неверный PIN-код"):
        delete_account(account_id=account.id, pin="0000")

    delete_account(account_id=account.id, pin="1234")

def test_delete_nonexistent_account():
    with pytest.raises(ValueError, match="Аккаунт с таким ID не найден"):
        delete_account(account_id=999999, pin="1234")