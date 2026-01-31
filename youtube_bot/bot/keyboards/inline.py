from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_format_keyboard(video_id: str) -> InlineKeyboardMarkup:
    """Format tanlash klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎥 Video (MP4)", callback_data=f"format:video:{video_id}"),
        InlineKeyboardButton(text="🎵 Audio (MP3)", callback_data=f"format:audio:{video_id}")
    )
    
    return builder.as_markup()

def get_quality_keyboard(video_id: str, format_type: str) -> InlineKeyboardMarkup:
    """Sifat tanlash klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    if format_type == "video":
        qualities = [
            ("1080p", "1080"),
            ("720p", "720"),
            ("480p", "480"),
            ("360p", "360")
        ]
    else:
        qualities = [
            ("320kbps", "320"),
            ("192kbps", "192"),
            ("128kbps", "128")
        ]
    
    for label, quality in qualities:
        builder.row(
            InlineKeyboardButton(
                text=label,
                callback_data=f"quality:{format_type}:{quality}:{video_id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data=f"back:{video_id}")
    )
    
    return builder.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Bekor qilish tugmasi"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    return builder.as_markup()

def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Admin panel klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")
    )
    builder.row(
        InlineKeyboardButton(text="🔥 Mashhur videolar", callback_data="admin:popular")
    )
    builder.row(
        InlineKeyboardButton(text="❌ Yopish", callback_data="admin:close")
    )
    
    return builder.as_markup()
