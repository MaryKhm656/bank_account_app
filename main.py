from models import BankAccount, PremiumAccount

# Обычный аккаунт
anna = BankAccount("Анна", pin=1234, balance=1000)

# Премиум аккаунт
bob = PremiumAccount("Боб", pin=4321, balance=500)

anna.deposit(200, pin=1234)
bob.deposit(500, pin=4321)

anna.transfer(300, pin=1234, recipient=bob)

print("\nИстория Анны:")
for entry in anna.show_history(pin=1234):
    print(entry)

print("\nИнформация о счёте Боба:")
print(bob.info(pin=4321))