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

To run this project, follow these steps:
    1. Download Python from the official site (https://www.python.org/downloads/) if it is not already installed.
    2. During installation, be sure to add Python to PATH.
    3. If you use Docker — ignore steps 4 and 8. Run the following commands with Docker:
        1. docker run --name redis -p 6379:6379 -d redis
        2. docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -d postgres
    4. If you are on Windows — install the Ubuntu distribution from the Microsoft Store (if an error occurs, run wsl --install in PowerShell), sign in and run the following commands:
        1. sudo apt update
        2. sudo apt install redis-server
        3. redis-server
    5. From the project root (CountryQuest) run: python -m venv .venv
    6. Run pip install -r requirements.txt. If an error occurs, check your location in the project. If you are even one level above or below the requirements.txt file, Python will not be able to install the project dependencies.
    7. Go to Telegram and find BotFather (https://t.me/BotFather), send /newbot and follow the instructions, then copy the token from the message:
        Done! Congratulations on your new bot. You will find it at t.me/CoQuestBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
        ...
        Use this token to access the HTTP API:
        [Your_bot_token]
        ...
        Keep your token secure and store it safely, it can be used by anyone to control your bot.
        For a description of the Bot API, see this page: https://core.telegram.org/bots/api
    8. Install PostgreSQL from the official site (https://www.postgresql.org/download/); during installation check the box to install pgAdmin 4. After installation open pgAdmin and create a database. Use the following format for your database URL: postgresql+asyncpg://[Database_owner_username]:[Database_owner_password]@localhost:[Database_port]/[Database_name]
    10. From the project root (CountryQuest) create a file named prod.env and fill it with the following:
        TOKEN=[Your_bot_token]
        DATABASE=[Your_database_connection_string]
        MODEL=[Your_AI_model_name]
        REDIS=redis://localhost:6379/
    11. Start the bot with python app/main.py. For running in dev mode use python -m app/main.py or python3 app/main.py

That's all, dear reader! From now on this project belongs to you...
