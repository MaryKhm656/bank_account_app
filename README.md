# BankAccount Project

Проект демонстрирует создание банковского приложения с использованием Python и SQLAlchemy. 
В основе — ООП, работа с базой данных, реализация PIN-защиты, и удобный консольный интерфейс.

## Что делает проект

- Создание аккаунтов с PIN-кодом
- Пополнение и снятие средств
- Переводы между аккаунтами
- История операций
- Просмотр баланса и информации об аккаунте
- Удаление аккаунта с подтверждением
- Проверка PIN-кода перед каждым действием

## Технологии и концепции

- Python 3
- ООП: классы, методы, инкапсуляция
- SQLAlchemy: подключение и работа с SQLite
- Datetime: фиксация операций по времени
- Структурирование кода: логика вынесена в отдельные модули

## Структура проекта

```bash
bank_account_app/
├── app/
│   ├── __init__.py
│   ├── database.py        # Настройка базы данных (SQLAlchemy)
│   ├── models.py          # Модели BankAccount и Operation
│   ├── functions.py       # Логика работы аккаунтов и операций
│   ├── main.py            # Консольное приложение
│   └── templates/         # (опционально) шаблоны для FastAPI в будущем
├── requirements.txt       # Список зависимостей
├── README.md              # Документация проекта
└── .gitignore             # Исключения для Git
```

##  Как запустить

1. Установите Python 3+
2. Скачайте/клонируйте проект
3. (Если нужно) установите зависимости:
   ```bash
   pip install sqlalchemy
   ```
4. Запустите `main.py`:
   ```bash
   python main.py
   ```

## Планы по развитию

Проект будет дополнен веб-интерфейсом с использованием FastAPI — для демонстрации навыков в создании REST API и современных Python-приложений.

## О пректе

Создан в рамках портфолио начинающего Python-разработчика.
Если вы рекрутер, тимлид или просто интересуетесь Python — welcome! 😊