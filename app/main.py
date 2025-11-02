import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from settings.config import settings
from handlers import messages
from handlers import callbacks
from data.models import Database
from data.redis import RedisManager

from middlewares.Database import DatabaseMiddleware
from middlewares.UserStatus import UserStatusMiddleware
from middlewares.SecureButton import SecureButtonMiddleware
from middlewares.Throtlling import ThrottlingMiddleware
from middlewares.GroupStatus import GroupStatusMiddleware

async def main():
    database = Database(settings.database.get_secret_value())
    redis = RedisManager()
    bot = Bot(token=settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    dp.message.middleware(DatabaseMiddleware(database.async_session))
    dp.message.middleware(UserStatusMiddleware())
    dp.message.middleware(GroupStatusMiddleware())
    dp.message.middleware(SecureButtonMiddleware(redis_manager=redis))
    dp.message.middleware(ThrottlingMiddleware(limit=3, interval=5))
    
    dp.callback_query.middleware(DatabaseMiddleware(database.async_session))
    dp.callback_query.middleware(UserStatusMiddleware())
    dp.callback_query.middleware(GroupStatusMiddleware())
    dp.callback_query.middleware(SecureButtonMiddleware(redis_manager=redis))
    
    dp.include_routers(
        messages.user,
        callbacks.user
    )
    
    try:
        os.system("alembic upgrade head")
        await bot.delete_webhook(drop_pending_updates=True)
        await redis.connect()
        print("Bot started!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await database.close()
        await redis.close()
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")