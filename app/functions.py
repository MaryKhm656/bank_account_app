from app.models import BankAccount
from app.database import SessionLocal

def create_account(owner: str, pin: str, initial_balance: float = 0.0):
    db = SessionLocal()
    try:
        existing_account = db.query(BankAccount).filter(BankAccount.owner == owner).first()
        if existing_account:
            raise ValueError("Такой аккаунт уже существует")
        account = BankAccount(owner=owner, balance=initial_balance)
        account.set_pin(pin)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    finally:
        db.close()

def deposit_to_account(account_id: int, amount: float, pin: str):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            raise ValueError("Аккаунт с таким ID не найден")
        account.deposit(amount=amount, pin=pin)
        db.commit()
        db.refresh(account)
        return account
    except ValueError as e:
        db.rollback()
        raise e
    finally:
        db.close()
        

def withdraw_from_account(account_id: int, amount: float, pin: str):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            raise ValueError("Аккаунт с таким ID не найден")
        account.withdraw(amount=amount, pin=pin)
        db.commit()
        db.refresh(account)
        return account
    except ValueError as e:
        db.rollback()
        raise e
    finally:
        db.close()
        
        
def transfer_money(from_id: int, to_id: int, amount: float, pin: str):
    db = SessionLocal()
    try:
        from_account = db.query(BankAccount).filter(BankAccount.id == from_id).first()
        to_account = db.query(BankAccount).filter(BankAccount.id == to_id).first()
        if not from_account:
            raise ValueError(f"Аккаунт с {from_id} не найден")
        if not to_account:
            raise ValueError(f"Аккаунт с {to_id} не найден")
        from_account.transfer(to_account=to_account, amount=amount, pin=pin)
        db.commit()
        db.refresh(from_account)
        db.refresh(to_account)
        return to_account, from_account
    except ValueError as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_history(account_id: int, pin: str):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            raise ValueError("Аккаунт с таким ID не найден")
        return account.get_history(pin)
    finally:
        db.close()
    
    
def get_account_balance(account_id: int, pin: str):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            raise ValueError("Аккаунт с таким ID не найден")
        if not account.check_pin(pin):
            raise ValueError("Неверный PIN-код")
        return f"{account.balance}"
    finally:
        db.close()


def get_account_by_id(account_id: int, pin: str):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            raise ValueError("Аккаунт с таким ID не найден")
        if not account.check_pin(pin):
            raise ValueError("Неверный PIN-код")
        return account
    finally:
        db.close()


def delete_account(account_id: int, pin: str):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            raise ValueError("Аккаунт с таким ID не найден")
        if not account.check_pin(pin):
            raise ValueError("Неверный PIN-код")

        db.delete(account)
        db.commit()
        return f"Аккаунт {account_id} успешно удалён"
    except ValueError as e:
        db.rollback()
        raise e
    finally:
        db.close()