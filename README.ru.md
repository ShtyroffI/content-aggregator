[English](README.md) | [Русский](README.ru.md)

---

# Телеграм-бот "Агрегатор контента"

Этот проект представляет собой телеграм-бота, написанного на Python с использованием библиотеки Aiogram 3. Бот позволяет пользователям подписываться на интересующие их темы и получать сводку (дайджест) свежих новостей по этим темам.

## Основные технологии

- **Язык:** Python 3.9
- **Основная библиотека для Telegram:** Aiogram 3
- **Работа с базой данных:** SQLAlchemy 2.0, Alembic (для миграций)
- **База данных:** PostgreSQL
- **Планировщик задач:** APScheduler
- **Парсинг:** Requests, BeautifulSoup4
- **Контейнеризация:** Docker, Docker-compose

## Функционал

- Подписка на темы с помощью команды `/subscribe <тема>`.
- Отписка от тем с помощью команды `/unsubscribe <тема>`.
- Просмотр своих подписок с помощью команды `/mysubscriptions`.
- Автоматическая рассылка дайджестов новостей по расписанию.

## Как запустить проект

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/ShtyroffI/content-aggregator.git
    cd content-aggregator
    ```

2.  **Создайте файл `.env`:**
    В корне проекта создайте файл `.env` со следующими переменными:
    ```
    BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
    DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
    ```
    *Убедитесь, что `user`, `password` и `dbname` совпадают с переменными в `docker-compose.yml`.

3.  **Запустите проект с помощью Docker-compose:**
    ```bash
    docker-compose up --build
    ```

4.  **Примените миграции базы данных:**
    В отдельном окне терминала выполните команду:
    ```bash
    docker-compose exec bot python -m alembic upgrade head
    ```

После этих шагов бот будет запущен и готов к работе.

## Автор

- **Имя:** Иван
- **GitHub:** [https://github.com/ShtyroffI](https://github.com/ShtyroffI)