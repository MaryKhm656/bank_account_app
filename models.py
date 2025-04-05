from datetime import datetime

class BankAccount:
    def __init__(self, owner, pin, balance=0):
        self.owner = owner
        self._pin = pin
        self._balance = balance
        self._history = []

    def _check_pin(self, pin):
        return pin == self._pin

    def deposit(self, amount, pin):
        if amount > 0:
            if self._check_pin(pin):
                self._balance += amount
                self._add_history(f"Пополнение +{amount}")
                print(f"Пополнено: {amount}. Новый баланс: {self._balance}")
            else:
                print("Неверный PIN!")
        else:
            print("Сумма должна быть больше 0!")

    def withdraw(self, amount, pin):
        if amount <= 0:
            print("Сумма снятия должна быть больше 0!")
        elif amount <= self._balance:
            if self._check_pin(pin):
                self._balance -= amount
                self._add_history(f"Снятие -{amount}")
                print(f"Снято {amount}. Новый баланс: {self._balance}")
            else:
                print("Неверный PIN!")
        else:
            print("Недостаточно средств!")

    def transfer(self, amount, pin, recipient):
        if amount <= 0:
            print("Сумма перевода должна быть больше 0!")
        elif amount <= self._balance:
            if self._check_pin(pin):
                self._balance -= amount
                recipient._balance += amount
                self._add_history(f"Перевод {amount} -> {recipient.owner}")
                print(f"Перевод выполнен! Новый баланс {self.owner}: {self._balance}")
            else:
                print("Неверный PIN!")
        else:
            print("Недостаточно средств!")

    def show_history(self, pin):
        if self._check_pin(pin):
            return self._history
        else:
            print("Неверный PIN!")

    def info(self, pin):
        if self._check_pin(pin):
            return f"Владелец: {self.owner}, Баланс: {self._balance}"
        else:
            print("Неверный PIN!")

    def _add_history(self, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._history.append(f"[{now}] {message}")


class PremiumAccount(BankAccount):
    def deposit(self, amount, pin):
        bonus = amount * 0.01
        total = amount + bonus
        if amount > 0:
            if self._check_pin(pin):
                self._balance += total
                self._add_history(f"Пополнение +{amount} (+1% бонус: {bonus:.2f})")
                print(f"Пополнено: {amount} (+бонус: {bonus:.2f}). Новый баланс: {self._balance}")
            else:
                print("Неверный PIN!")
        else:
            print("Сумма должна быть больше 0!")