from database import init_db
from functions import (
    create_account, deposit_to_account, withdraw_from_account,
    transfer_money, get_account_balance, get_account_by_id, get_history, delete_account
)

init_db()

def main():
    while True:
        print("\nДобро пожаловать в банковское приложение!")
        print("1. Создать аккаунт")
        print("2. Пополнить счёт")
        print("3. Снять со счёта")
        print("4. Перевести деньги")
        print("5. Посмотреть баланс")
        print("6. История операций")
        print("7. Информация об аккаунте")
        print("8. Удаление аккаунта")
        print("0. Выход")
        
        choice = input("Выберите действие:")
        
        try:
            match choice:
                case "1":
                    owner = input("Введите имя владельца: ")
                    pin = input("Придумайте PIN-код: ")
                    initial = float(input("Начальный баланс (можно 0): "))
                    account = create_account(owner, pin, initial)
                    print(f"\nАккаунт создан! Ваш ID: {account.id}")
                    print("-" * 40)
                case "2":
                    acc_id = int(input("Введите ID аккаунта: "))
                    pin = input("Введите PIN-код: ")
                    amount = float(input("Сумма пополнения: "))
                    deposit_to_account(acc_id, amount, pin)
                    print("Счёт пополнен!")
                    print("-" * 40)
                case "3":
                    acc_id = int(input("Введите ID аккаунта: "))
                    pin = input("Введите PIN-код: ")
                    amount = float(input("Сумма снятия: "))
                    withdraw_from_account(acc_id, amount, pin)
                    print("Снятие прошло успешно!")
                    print("-" * 40)
                case "4":
                    from_id = int(input("ID отправителя: "))
                    to_id = int(input("ID получателя: "))
                    pin = input("PIN отправителя: ")
                    amount = float(input("Сумма перевода: "))
                    transfer_money(from_id, to_id, amount, pin)
                    print("Перевод выполнен!")
                    print("-" * 40)
                case "5":
                    acc_id = int(input("ID аккаунта: "))
                    pin = input("Введите PIN-код: ")
                    balance = get_account_balance(acc_id, pin)
                    print(f"Баланс: {balance}")
                    print("-" * 40)
                case "6":
                    acc_id = int(input("ID аккаунта: "))
                    pin = input("Введите PIN-код: ")
                    history = get_history(acc_id, pin)
                    for h in history:
                        print(f"{h[2]} — {h[0]}: {h[1]}")
                    print("-" * 40)
                case "7":
                    acc_id = int(input("ID аккаунта: "))
                    pin = input("Введите PIN-код: ")
                    info = get_account_by_id(acc_id, pin)
                    print(info)
                    print("-" * 40)
                case "8":
                    print("Вы уверены что хотите удалить аккаунт?")
                    solution = input("Введите 'Да' или 'Нет': ").lower()
                    if solution == 'да':
                        acc_id = int(input("ID аккаунта: "))
                        pin = input("Введите PIN-код: ")
                        delete_account(acc_id, pin)
                        print("Аккаунт успешно удален!")
                        print("-" * 40)
                    elif solution == 'нет':
                        print("Вы передумали удалять аккаунт")
                        print("-" * 40)
                    else:
                        print("Неверный ответ. Операция отменена.")
                        print("-" * 40)
                case "0":
                    print("Выход из программы. До свидания!")
                    break
                case _:
                    print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"Ошибка: {e}")
            
if __name__ == "__main__":
    main()