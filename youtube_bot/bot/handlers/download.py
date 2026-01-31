from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
import os

from bot.services.youtube import YouTubeService
from bot.keyboards.inline import get_format_keyboard, get_quality_keyboard, get_cancel_keyboard
from bot.config import config
from bot.database.crud import DownloadCRUD, UserCRUD
from bot.utils.helpers import sanitize_filename

router = Router()
youtube_service = YouTubeService()

class DownloadStates(StatesGroup):
    """Yuklab olish holatlari"""
    waiting_for_url = State()
    selecting_format = State()
    selecting_quality = State()

@router.message(F.text.regexp(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'))
async def handle_youtube_url(message: Message, state: FSMContext, session: AsyncSession):
    """YouTube URL qabul qilish"""
    # Ban tekshiruvi
    if await UserCRUD.is_user_banned(session, message.from_user.id):
        await message.answer("❌ Siz botdan foydalanish huquqidan mahrum qilingansiz.")
        return
    
    url = message.text.strip()
    
    if not youtube_service.validate_url(url):
        await message.answer("❌ Noto'g'ri YouTube havolasi. Iltimos, qaytadan urinib ko'ring.")
        return
    
    # Video ma'lumotlarini olish
    status_msg = await message.answer("⏳ Video ma'lumotlari yuklanmoqda...")
    
    video_info = await youtube_service.get_video_info(url)
    
    if not video_info:
        await status_msg.edit_text("❌ Video topilmadi yoki ma'lumotlarni yuklab bo'lmadi.")
        return
    
    # Ma'lumotlarni saqlash
    await state.update_data(video_info=video_info, video_url=url)
    
    # Video ma'lumotlarini ko'rsatish
    duration_min = video_info['duration'] // 60
    duration_sec = video_info['duration'] % 60
    
    info_text = (
        f"🎬 <b>{video_info['title']}</b>\n\n"
        f"👤 Kanal: {video_info['uploader']}\n"
        f"⏱ Davomiyligi: {duration_min}:{duration_sec:02d}\n"
        f"👁 Ko'rishlar: {video_info['view_count']:,}\n\n"
        f"📥 Formatni tanlang:"
    )
    
    await status_msg.delete()
    await message.answer_photo(
        photo=video_info['thumbnail'],
        caption=info_text,
        reply_markup=get_format_keyboard(video_info['id'])
    )
    
    await state.set_state(DownloadStates.selecting_format)

@router.callback_query(F.data.startswith("format:"))
async def handle_format_selection(callback: CallbackQuery, state: FSMContext):
    """Format tanlash"""
    _, format_type, video_id = callback.data.split(":")
    
    await state.update_data(format_type=format_type)
    
    format_name = "Video" if format_type == "video" else "Audio"
    await callback.message.edit_caption(
        caption=f"📊 {format_name} sifatini tanlang:",
        reply_markup=get_quality_keyboard(video_id, format_type)
    )
    
    await state.set_state(DownloadStates.selecting_quality)
    await callback.answer()

@router.callback_query(F.data.startswith("quality:"))
async def handle_quality_selection(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Sifat tanlash va yuklab olishni boshlash"""
    _, format_type, quality, video_id = callback.data.split(":")
    
    data = await state.get_data()
    video_info = data['video_info']
    video_url = data['video_url']
    
    # Yuklanish xabari
    await callback.message.edit_caption(
        caption="⏬ Yuklab olinmoqda... Iltimos kuting..."
    )
    
    # Fayl yo'lini aniqlash
    safe_title = sanitize_filename(video_info['title'])
    file_extension = "mp4" if format_type == "video" else "mp3"
    output_path = os.path.join(config.DOWNLOADS_DIR, f"{video_id}_{quality}.{file_extension}")
    
    # Yuklab olish
    if format_type == "video":
        file_path = await youtube_service.download_video(video_id, quality, output_path)
    else:
        file_path = await youtube_service.download_audio(video_id, quality, output_path)
    
    if not file_path or not os.path.exists(file_path):
        await callback.message.edit_caption(
            caption="❌ Yuklab olishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        )
        await callback.answer()
        return
    
    # Fayl hajmini tekshirish
    file_size = os.path.getsize(file_path)
    if file_size > config.MAX_FILE_SIZE:
        await callback.message.edit_caption(
            caption=f"❌ Fayl hajmi juda katta ({file_size // 1024 // 1024} MB). Telegram chegarasi: 2GB"
        )
        os.remove(file_path)
        await callback.answer()
        return
    
    # Faylni yuborish
    await callback.message.edit_caption(caption="📤 Foydalanuvchiga yuborilmoqda...")
    
    file_to_send = FSInputFile(file_path, filename=f"{safe_title}.{file_extension}")
    
    if format_type == "video":
        await callback.message.answer_video(
            video=file_to_send,
            caption=f"✅ <b>{video_info['title']}</b>\n\n📹 Sifat: {quality}p"
        )
    else:
        await callback.message.answer_audio(
            audio=file_to_send,
            caption=f"✅ <b>{video_info['title']}</b>\n\n🎵 Sifat: {quality}kbps",
            title=video_info['title'],
            performer=video_info['uploader']
        )
    
    # Statistikaga qo'shish
    await DownloadCRUD.create_download(
        session,
        user_id=callback.from_user.id,
        video_id=video_id,
        video_title=video_info['title'],
        video_url=video_url,
        format_type=format_type,
        quality=quality,
        file_size=file_size,
        duration=video_info['duration']
    )
    
    # Tozalash
    await callback.message.delete()
    if os.path.exists(file_path):
        os.remove(file_path)
    await state.clear()
    await callback.answer("✅ Muvaffaqiyatli yuklandi!")

@router.callback_query(F.data.startswith("back:"))
async def handle_back(callback: CallbackQuery, state: FSMContext):
    """Orqaga qaytish"""
    video_id = callback.data.split(":")[1]
    
    await callback.message.edit_caption(
        caption="📥 Formatni tanlang:",
        reply_markup=get_format_keyboard(video_id)
    )
    
    await state.set_state(DownloadStates.selecting_format)
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    """Jarayonni bekor qilish"""
    await callback.message.delete()
    await state.clear()
    await callback.answer("❌ Bekor qilindi")
