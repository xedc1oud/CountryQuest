# CountryQuest - Telegram bot
# This project is licensed under the MIT License.
# Created by xedc1oud in 2025.

Welcome, dear reader! In front of you is a Telegram bot written in Python using various libraries, including aiogram, aioredis, alembic, asyncpg. This bot is an unrealized project and will probably never be completed, since its development is finished. However, I decided to publish it on GitHub.

This project uses the following technologies:
    - SQL
    - Redis
    - Alembic
    - Python

You may want to know the project tree you'll be working with:
    CountryQuest/
    ├── .venv/
    ├── .vscode/
    ├── alembic/
    │   ├── versions/
    │   ├── env.py
    │   ├── README
    │   └── script.py.mako
    ├── app/
    │   ├── data/
    │   │   ├── models.py
    │   │   ├── redis.py
    │   │   └── requests.py
    │   ├── handlers/
    │   │   ├── callbacks.py
    │   │   └── messages.py
    │   └── keyboards/
    │   │   ├── inline.py
    │   │   ├── security.py
    │   │   └── pagination.py
    │   ├── middlewares/
    │   │   ├── SecureButton.py
    │   │   ├── Database.py
    │   │   ├── Throtlling.py
    │   │   ├── GroupStatus.py
    │   │   └── UserStatus.py
    │   ├── photos/
    │   ├── settings/
    │   │   └── config.py
    │   └── utils/
    │       ├── helpers.py
    │       ├── states.py
    │       └── main.py
    ├── .gitignore
    ├── alembic.ini
    ├── LICENSE
    ├── prod.env
    ├── README.md
    └── requirements.txt

Для запуска данного проекта, следуй следующим пунктам:
    1. Скачай Python с официального сайта (https://www.python.org/downloads/), если он еще не установлен
    2. При установке обязательно добавь Python в PATH
    3. Если ты используешь Docker - не изучай 4 и 8 пункт. Выполни следующие команды в Docker:
        1. docker run --name redis -p 6379:6379 -d redis
        2. docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -d postgres
    4. Если ты на Windows - установи из Microsoft Store дистрибутив Ubuntu (Если возникла ошибка, в PowerShell напиши --wsl install), выполни вход и напиши следующие команды:
        1. sudo apt update
        2. sudo apt install redis-server
        3. redis-server
    5. Находясь в корневом файле проекта (CountryQuest) выполни команду "python -m venv .venv" 
    6. Выполни команду "pip install -r requirements.txt", если происходит ошибка, обрати внимание на свое расположение в проекте. Если ты будешь находиться хотябы на уровень выше или ниже файла requirements.txt - Python не сможет установить зависимости проекта.
    7. Зайди в Telegram и найди BotFather (https://t.me/BotFather), напиши команду /newbot и выполни все указания, а затем скопируй токен из данного сообщения:
        Done! Congratulations on your new bot. You will find it at t.me/CoQuestBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
        ...
        Use this token to access the HTTP API:
        [Токен_от_твоего_бота]
        ...
        Keep your token secure and store it safely, it can be used by anyone to control your bot.
        For a description of the Bot API, see this page: https://core.telegram.org/bots/api
    8. Установи postgreSQL с официального сайта (https://www.postgresql.org/download/), при установке нажми галочку с установкой pgAdmin 4. После установки зайди в программу и создай базу данных. Подставь данные твоей базы данных под форму: postgresql+asyncpg://[Имя_владельца_базы_данных]:[Пароль_владельца_базы_данных]@localhost:[Порт_базы_данных]/[Название_базы_данных]
    10. Находясь в корневом файле проекта (CountryQuest) создай файл prod.env и заполни туда следующие данные:
        TOKEN=[Токен_от_твоего_бота]
        DATABASE=[Ключ_от_твоей_базы_данных]
        MODEL=[Название_модели_твоего_ИИ]
        REDIS=redis://localhost:6379/
    11. Запусти бота командой "python app/main.py". Однако, для запуска проекта в dev-режиме, выполни команду "python -m app/main.py" или "python3 app/main.py"

Вот и все, дорогой читатель! Данный проект отныне подчиняется лишь тебе...