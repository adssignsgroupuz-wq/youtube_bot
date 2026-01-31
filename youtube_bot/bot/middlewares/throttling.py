from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import time

class ThrottlingMiddleware(BaseMiddleware):
    """
    Spam oldini olish uchun middleware.
    Har bir foydalanuvchi belgilangan vaqt ichida faqat bir marta so'rov yuborishi mumkin.
    """
    
    def __init__(self, time_limit: int = 2):
        """
        Args:
            time_limit: Ikki so'rov orasidagi minimal vaqt (sekundlarda)
        """
        self.time_limit = time_limit
        self.user_timestamps: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Throttling tekshiruvi"""
        user_id = event.from_user.id
        current_time = time.time()
        
        # Oxirgi so'rov vaqtini tekshirish
        last_time = self.user_timestamps.get(user_id, 0)
        
        if current_time - last_time < self.time_limit:
            # Juda tez so'rov yuborildi
            if isinstance(event, Message):
                await event.answer(
                    "⏳ Iltimos, biroz kuting va qaytadan urinib ko'ring.",
                    show_alert=False
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "⏳ Juda tez! Biroz kuting.",
                    show_alert=True
                )
            return
        
        # Vaqtni yangilash
        self.user_timestamps[user_id] = current_time
        
        # Handlerni davom ettirish
        return await handler(event, data)
