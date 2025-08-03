import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Импортируем наши модули
from handlers import user_commands
from scheduler.jobs import send_digest

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Функция для настройки меню команд
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/mysubscriptions', description='Мои подписки'),
        BotCommand(command='/subscribe', description='Подписаться на тему'),
        BotCommand(command='/unsubscribe', description='Отписаться от темы')
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутер с хэндлерами
    dp.include_router(user_commands.router)
    
    # Устанавливаем меню команд
    await set_main_menu(bot)

    # Инициализация и запуск планировщика
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_digest, trigger='cron', hour='10, 22', minute='0', args=(bot,))
    scheduler.start()

    # Запускаем поллинг
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
