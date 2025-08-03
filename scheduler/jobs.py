from aiogram import Bot
from sqlalchemy import select

import content_parser as parser
from db.engine import async_session_factory
from db.models import Subscription

async def send_digest(bot: Bot):
    print("Начинаю рассылку дайджеста...")
    html_content = parser.get_html(parser.URL)
    if not html_content:
        print("Не удалось получить HTML для парсинга.")
        return
    
    articles = parser.parse_articles(html_content)
    if not articles:
        print("Не удалось найти статьи для рассылки.")
        return
    
    print(f"Найдено {len(articles)} статей. Начинаю обработку.")

    async with async_session_factory() as session:
        query = select(Subscription.keyword).distinct()
        result = await session.execute(query)
        keywords = result.scalars().all()
    
        if not keywords:
            print("В базе нет ни одной активной подписки.")
            return

        print(f"Найдены активные подписки на ключевые слова: {keywords}")

        for article in articles:
            for keyword in keywords:
                if keyword.lower() in article['title'].lower():
                    stmt = select(Subscription).where(Subscription.keyword == keyword)
                    subscribers_result = await session.execute(stmt)
                    subscribers = subscribers_result.scalars().all()
                    for sub in subscribers:
                        try:
                            await bot.send_message(
                                chat_id=sub.user_id,
                                text=f"Новая статья по вашей подписке '{keyword}'!\n\n{article['title']}\n{article['link']}",
                                disable_web_page_preview=True
                            )
                        except Exception as e:
                            print(f"Не удалось отправить сообщение пользователю {sub.user_id}: {e}")
                    break
    
    print("Рассылка дайджеста завершена.")