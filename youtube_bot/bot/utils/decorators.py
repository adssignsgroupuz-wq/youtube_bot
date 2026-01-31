from functools import wraps
from aiogram.types import Message, CallbackQuery
from bot.config import config

def admin_only(func):
    """Faqat adminlar uchun"""
    @wraps(func)
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        user_id = event.from_user.id
        
        if user_id not in config.ADMIN_IDS:
            if isinstance(event, Message):
                await event.answer("❌ Bu buyruq faqat adminlar uchun!")
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ Ruxsat yo'q!", show_alert=True)
            return
        
        return await func(event, *args, **kwargs)
    
    return wrapper
