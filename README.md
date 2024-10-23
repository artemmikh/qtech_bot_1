
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastApi](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

# Информационный Telegram-бот с админ-зоной
### Описание проекта
Проект представляет собой Telegram-бот с административной панелью. В интерфейсе бота пользователь может указать, посещает ли он московский офис. В зависимости от выбора, пользователю отображается список информационных кнопок. При нажатии на кнопки сотрудник получает необходимую информацию. 
Названия и содержимое кнопок загружаются из базы данных. Администратор может добавлять или изменять их через админ-зону.

Код бота написан с использованием библиотеки python-telegram-bot, админ-зона создана с использованием FastAPI и HTML шаблонов.

### Протестировать бота можно [по этой ссылке](https://t.me/test_qtech_bot).

## Запуск проекта

1. Клонируйте репозиторий и перейдите в него в командной строке:

    ```bash
    git clone git@github.com:artemmikh/qtech_bot_1.git
    ```

2. Перейдите в директорию с кодом проекта и создайте виртуальное окружение:

    ```bash
    python3 -m venv venv
    ```

3. Активируйте виртуальное окружение:

    * Для Linux/macOS:

        ```bash
        source venv/bin/activate
        ```

    * Для Windows:

        ```bash
        source venv/scripts/activate
        ```

4. Обновите менеджер пакетов `pip`:

    ```bash
    python -m pip install --upgrade pip
    ```

5. Установите зависимости из файла `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

6. В корне проекта создайте файл `.env` и добавьте в него следующие данные (замените `EXAMPLE_BOT_TOKEN` на ваш реальный токен):

    ```bash
    BOT_TOKEN=EXAMPLE_BOT_TOKEN
    APP_TITLE=Админ-панель
    DATABASE_URL=sqlite+aiosqlite:///./Qtech_bot.db
    BOT_DATABASE_URL=sqlite:///../Qtech_bot.db
    SECRET=YOUR_SECRET
    ```

7. Примените миграции базы данных:

    ```bash
    alembic upgrade head
    ```

8. Запустите Telegram-бота:

    ```bash
    python bot/main.py
    ```

9. Запустите локальный сервер FastAPI:

    ```bash
    uvicorn app.main:app --reload
    ```

### Документация
После запуска документация будет доступна по [этой ссылке](http://127.0.0.1:8000/docs).
