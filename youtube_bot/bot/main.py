import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.handlers import start, download, admin, playlist
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.database import DatabaseMiddleware
from bot.database.database import init_db

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Asosiy funksiya"""
    # Databaseni ishga tushirish
    await init_db()
    logger.info("Database muvaffaqiyatli ishga tushdi!")
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Middlewarelarni ulash
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.message.middleware(ThrottlingMiddleware(time_limit=2))
    dp.callback_query.middleware(ThrottlingMiddleware(time_limit=1))
    
    # Routerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(download.router)
    dp.include_router(admin.router)
    dp.include_router(playlist.router)
    
    logger.info("Bot ishga tushdi!")
    
    # Polling rejimida ishga tushirish
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi!")
