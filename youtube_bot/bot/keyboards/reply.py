from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy klaviatura"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="📊 Mening statistikam"),
        KeyboardButton(text="ℹ️ Yordam")
    )
    
    return builder.as_markup(resize_keyboard=True)
