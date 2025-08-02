import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import BotCommand
from sqlalchemy import select
from db.engine import async_session_factory
from db.models import User, Subscription

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def handle_start(message: types.Message):
    await message.answer("Привет! 👋\nЯ бот-агрегатор.")

@dp.message(Command(commands=['subscribe']))
async def handle_subscribe(message: types.Message, command: CommandObject):
    keyword = command.args

    if not keyword:
        await message.answer("Пожалуйста, укажите ключевое слово после команды.\nНапример: /subscribe Python")
        return
    
    try:
        async with async_session_factory() as session:
            user = await session.get(User, message.from_user.id)
            if not user:
                user = User(
                    user_id = message.from_user.id,
                    username = message.from_user.username,
                    first_name = message.from_user.first_name
                )
                session.add(user)

            stmt = select(Subscription).where(
                Subscription.user_id == user.user_id,
                Subscription.keyword == keyword
            )
            existing_sunscription = await session.scalar(stmt)

            if existing_sunscription:
                await message.answer(f"Вы уже подписаны на '{keyword}'.")
            else:
                new_subscription = Subscription(user_id = user.user_id, keyword=keyword)
                session.add(new_subscription)
                await session.commit()
                await message.answer(f"Вы успешно подписались на '{keyword}'!")

    except Exception as e:
        print(f"Произошла ошибка при подписке: {e}")
        await message.answer("Произошла ошибка при обработке вашей подписки. Попробуйте позже.")

@dp.message(Command(commands=['mysubscriptions']))
async def handle_mysubscriptions(message: types.Message):
    try:
        async with async_session_factory() as session:
            stmt = select(Subscription).where(Subscription.user_id == message.from_user.id)
            result = await session.execute(stmt)
            subscriptions = result.scalars().all()

            if subscriptions:
                subscription_keywords = [sub.keyword for sub in subscriptions]
                response_text = "Ваши активные подписки:\n\n" + "\n".join(f"- {keyword}" for keyword in subscription_keywords)
                await message.answer(response_text)
            else:
                await message.answer("У вас пока нет активных подписок...")
    except Exception as e:
        print(f"Произошла ошибка при просмотре подписок: {e}")
        await message.answer("Произошла ошибка при проверке ваших подписок. Попробуйте позже.")

@dp.message(Command(commands=['unsubscribe']))
async def handle_unsubscribe(message: types.Message, command: CommandObject):
    keyword = command.args

    if not keyword:
        await message.answer("Пожалуйста, укажите ключевое слово после команды.\nНапример: /unsubscribe Python")
        return
    
    try:
        async with async_session_factory() as session:
            stmt = select(Subscription).where(
                Subscription.user_id == message.from_user.id,
                Subscription.keyword == keyword
            )
            subscription_to_delete = await session.scalar(stmt)

            if subscription_to_delete:
                await session.delete(subscription_to_delete)
                await session.commit()
                await message.answer(f"Вы успешно отписались от '{keyword}'.")
            else:
                await message.answer(f"Вы и так не были подписаны на '{keyword}'.")
            
    except Exception as e:
        print(f"Произошла ошибка при подписке: {e}")
        await message.answer("Произошла ошибка при обработке вашей подписки. Попробуйте позже.")


@dp.message()
async def handle_echo(message: types.Message):
    await message.answer(message.text)

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/mysubscriptions', description='Мои подписки'),
        BotCommand(command='/subscribe', description='Подписаться на тему'),
        BotCommand(command='/unsubscribe', description='Отписаться от темы')
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    await set_main_menu(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())