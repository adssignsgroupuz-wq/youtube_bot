from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio

from bot.services.youtube import YouTubeService
from bot.keyboards.inline import get_cancel_keyboard

router = Router()
youtube_service = YouTubeService()

@router.message(F.text.regexp(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*(list=|playlist\?).*'))
async def handle_playlist_url(message: Message):
    """Playlist URL ni aniqlash"""
    url = message.text.strip()
    
    status_msg = await message.answer(
        "📋 Playlist ma'lumotlari yuklanmoqda...",
        reply_markup=get_cancel_keyboard()
    )
    
    # Playlist ma'lumotlarini olish
    playlist_info = await youtube_service.get_playlist_info(url)
    
    if not playlist_info:
        await status_msg.edit_text("❌ Playlist topilmadi yoki ma'lumotlarni yuklab bo'lmadi.")
        return
    
    videos_count = len(playlist_info['videos'])
    
    info_text = (
        f"📋 <b>{playlist_info['title']}</b>\n\n"
        f"📹 Videolar soni: {videos_count}\n\n"
        f"⚠️ <b>Diqqat:</b>\n"
        f"Playlist yuklab olish uzoq vaqt olishi mumkin.\n"
        f"Har bir video alohida yuboriladi.\n\n"
        f"Davom etishni xohlaysizmi?"
    )
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Ha, boshlash", callback_data=f"playlist:start:{url}"),
        InlineKeyboardButton(text="❌ Yo'q", callback_data="cancel")
    )
    
    await status_msg.edit_text(info_text, reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("playlist:start:"))
async def start_playlist_download(callback: CallbackQuery):
    """Playlist yuklab olishni boshlash"""
    url = callback.data.split(":", 2)[2]
    
    await callback.message.edit_text(
        "⏬ Playlist yuklab olish boshlandi!\n\n"
        "Har bir video alohida yuboriladi.\n"
        "Bu jarayon uzoq davom etishi mumkin..."
    )
    
    # Bu yerda har bir videoni yuklab olish logikasi bo'ladi
    # Hozircha faqat xabar ko'rsatamiz
    await callback.answer("✅ Jarayon boshlandi!")
