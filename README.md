[English](README.md) | [Русский](README.ru.md)

---

# Content Aggregator Telegram Bot

This project is a Telegram bot written in Python using the Aiogram 3 library. The bot allows users to subscribe to topics of interest and receive a digest of fresh news on these topics.

## Core Technologies

- **Language:** Python 3.9
- **Telegram Bot Framework:** Aiogram 3
- **Database Interaction:** SQLAlchemy 2.0 (ORM), Alembic (for migrations)
- **Database:** PostgreSQL
- **Task Scheduler:** APScheduler
- **Web Scraping:** Requests, BeautifulSoup4
- **Containerization:** Docker, Docker-compose

## Features

- Subscribe to topics using the `/subscribe <topic>` command.
- Unsubscribe from topics using the `/unsubscribe <topic>` command.
- View your current subscriptions with the `/mysubscriptions` command.
- Automatic scheduled delivery of news digests.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ShtyroffI/content-aggregator.git
    cd content-aggregator
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root of the project with the following variables. You can copy `example.env` (if you create one) for a template.
    ```
    BOT_TOKEN=YOUR_TOKEN_FROM_BOTFATHER
    DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
    ```
    *Ensure that `user`, `password`, and `dbname` match the environment variables in your `docker-compose.yml` file.

3.  **Run the project with Docker-compose:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply database migrations:**
    In a separate terminal window, run the following command to apply the database migrations:
    ```bash
    docker-compose exec bot python -m alembic upgrade head
    ```

After these steps, the bot will be up and running.

## Author

- **Name:** Ivan
- **GitHub:** [https://github.com/ShtyroffI](https://github.com/ShtyroffI)