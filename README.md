# Bank Account API

FastAPI-приложение для управления банковскими аккаунтами. Можно создавать аккаунты, пополнять счёт, снимать деньги, переводить между счетами и удалять аккаунт.

##  Возможности

- Создание нового аккаунта
- Получение информации об аккаунте по ID и PIN
- Пополнение счёта
- Снятие средств
- Перевод между аккаунтами
- Удаление аккаунта (по PIN)

---

## Используемые технологии

- **Python 3.11+**
- **FastAPI** — создание REST API
- **SQLAlchemy** — ORM для работы с БД
- **SQLite** — локальная база данных
- **Pydantic** — валидация и сериализация данных
- **Uvicorn** — ASGI-сервер для запуска FastAPI
- **Pytest** — модульное тестирование

## Структура проекта

```bash
bank_account_app/                  # Основная директория проекта
├── app/                           # Код приложения
│   ├── api/                       # Роуты API
│   │   └── routes.py              # Эндпоинты: создание, получение, пополнение и т.д.
│   ├── schemas/                   # Схемы Pydantic
│   │   └── account.py             # Модели запросов и ответов
│   ├── templates/                 # (Планируется подключение визуального интерфейса)
│   ├── __init__.py
│   ├── database.py                # Подключение к базе данных
│   ├── functions.py               # Бизнес-логика аккаунтов
│   ├── main.py                    # Запуск приложения FastAPI
│   └── models.py                  # Модели SQLAlchemy (BankAccount)
│
├── tests/                         # Модульные тесты
│   ├── __init__.py
│   ├── conftest.py                # Общие фикстуры (например, создание аккаунтов)
│   ├── test_logic.py              # Тесты бизнес-логики
│   └── test_routes.py             # Тесты API эндпоинтов (в т.ч. с ошибками и parametrize)
│
├── old_main.py                    # Консольное мини-приложение (первая реализация логики)
├── .gitignore
├── README.md
└── requirements.txt               # Зависимости проекта
```

## Запуск проекта

1. Клонируй репозиторий:
 
```bash
   git clone https://github.com/MaryKhm656/bank_account_app.git
   cd bank_account_app
   ```
2. Установи зависимости:

```bash
   pip install -r requirements.txt
   ```

3. Запусти сервер:

   ```bash
   uvicorn app.main:app --reload
   ```
   
# Примеры запросов

## Создать аккаунт:
POST /accounts/

```bash
{
  "owner": "Alice",
  "pin": "1234",
  "balance": 500.0
}
```

## Пополнение счета:
POST /accounts/1/deposit
```bash
{
  "amount": 1000.0,
  "pin": "1234"
}
```

## Снять деньги:
POST /accounts/1/withdraw
```bash
{
  "amount": 500.0,
  "pin": "1234"
}
```

## Перевод между счетами:
POST /accounts/1/2/transfer
```bash
{
  "amount": 300.0,
  "pin": "1234"
}
```

## Удаление аккаунта:
DELETE /accounts/delete/1?pin=1234

# Запуск тестов

```bash
  pytest tests/
```
## Тестируются:

- Основные сценарии (создание, перевод, пополнение и т.д.)
- Ошибки (неверный PIN, превышение баланса, перевод на несуществующий аккаунт, повторное удаление)
- Используется @pytest.mark.parametrize для лаконичных и расширяемых тестов

## Планы на будущее:
- Добавление визуального интерфейса
- Поддержка PostgreSQL
- Docker и деплой