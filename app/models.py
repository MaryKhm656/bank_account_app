from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class BankAccount(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    owner = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    _pin = Column("pin", String, nullable=False)
    
    operations = relationship("Operation", back_populates="account", cascade="all, delete-orphan")
    
    def set_pin(self, pin: str):
        self._pin = pin
        
    def check_pin(self, pin: str):
        return self._pin == pin
    
    def deposit(self, amount, pin):
        if not self.check_pin(pin):
            raise ValueError("Неверный PIN-код")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount
        self.add_operation("Пополнение", amount)
        
    def withdraw(self, amount, pin):
        if not self.check_pin(pin):
            raise ValueError("Неверный PIN-код")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount < self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        self.add_operation("Снятие", amount)

    def transfer(self, to_account, amount, pin):
        if not self.check_pin(pin):
            raise ValueError("Неверный PIN-код")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")

        self.balance -= amount
        to_account.balance += amount

        self.add_operation(f"Перевод на аккаунт {to_account.id}", -amount)
        to_account.add_operation(f"Перевод от аккаунта {self.id}", amount)
        
    def add_operation(self, type_, amount):
        op = Operation(type=type_, amount=amount, timestamp=datetime.utcnow(), account=self)
        self.operations.append(op)
        
    def get_history(self):
        return [(op.type, op.amount, op.timestamp.strftime("%Y-%m-%d %H:%M:%S")) for op in self.operations]
    
    
class Operation(Base):
    __tablename__ = "operations"
    
    id = Column(Integer, primary_key=True)
    type = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    
    account = relationship("BankAccount", back_populates="operations")