from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.crud import UserCRUD
from bot.keyboards.reply import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    """Start komandasi handleri"""
    # Foydalanuvchini yaratish/yangilash
    user = await UserCRUD.get_or_create_user(
        session,
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    )
    
    # Ban tekshiruvi
    if user.is_banned:
        await message.answer("❌ Siz botdan foydalanish huquqidan mahrum qilingansiz.")
        return
    
    welcome_text = (
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "Men YouTube video va audio yuklab olish botiman.\n\n"
        "📹 <b>Qanday ishlatiladi:</b>\n"
        "1. YouTube video linkini yuboring\n"
        "2. Format tanlang (Video yoki Audio)\n"
        "3. Sifatni tanlang\n"
        "4. Yuklashni kuting!\n\n"
        "💡 <i>Misol:</i> https://youtu.be/dQw4w9WgXcQ\n\n"
        "📋 <b>Qo'shimcha imkoniyatlar:</b>\n"
        "• Playlist yuklab olish\n"
        "• Turli sifatlarda yuklab olish\n"
        "• Audio formatda yuklab olish\n\n"
        "❓ Yordam kerakmi? /help buyrug'ini yuboring"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@router.message(F.text == "ℹ️ Yordam")
async def cmd_help(message: Message):
    """Yordam komandasi"""
    help_text = (
        "📖 <b>Yordam</b>\n\n"
        "<b>Asosiy funksiyalar:</b>\n"
        "• Video yuklab olish - YouTube video linkini yuboring\n"
        "• Audio yuklab olish - MP3 formatda yuklab olish\n"
        "• Playlist yuklab olish - Butun playlistni yuklab olish\n\n"
        "<b>Qo'llab-quvvatlanadigan formatlar:</b>\n"
        "🎥 Video: 1080p, 720p, 480p, 360p\n"
        "🎵 Audio: 320kbps, 192kbps, 128kbps\n\n"
        "<b>Cheklovlar:</b>\n"
        "• Maksimal fayl hajmi: 2GB\n"
        "• So'rovlar orasida 2 soniya kutish\n\n"
        "❓ Savollaringiz bo'lsa, @yoursupport ga murojaat qiling"
    )
    await message.answer(help_text)

@router.message(F.text == "📊 Mening statistikam")
async def cmd_my_stats(message: Message, session: AsyncSession):
    """Foydalanuvchi statistikasi"""
    from bot.database.crud import DownloadCRUD
    
    downloads = await DownloadCRUD.get_user_downloads(session, message.from_user.id, limit=5)
    
    if not downloads:
        await message.answer("📊 Hali yuklab olishlar yo'q.")
        return
    
    stats_text = f"📊 <b>Sizning statistikangiz</b>\n\n"
    stats_text += f"📥 Jami yuklab olishlar: <b>{len(downloads)}</b>\n\n"
    stats_text += "<b>Oxirgi 5 ta yuklab olish:</b>\n\n"
    
    for i, dl in enumerate(downloads, 1):
        stats_text += f"{i}. {dl.video_title[:40]}...\n"
        stats_text += f"   📅 {dl.downloaded_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    
    await message.answer(stats_text)
