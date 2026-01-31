from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from bot.database.crud import UserCRUD, DownloadCRUD, StatisticsCRUD
from bot.utils.decorators import admin_only
from bot.keyboards.inline import get_admin_keyboard

router = Router()

@router.message(Command("admin"))
@admin_only
async def cmd_admin(message: Message):
    """Admin panel"""
    await message.answer(
        "🔐 <b>Admin Panel</b>\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=get_admin_keyboard()
    )

@router.callback_query(F.data == "admin:stats")
@admin_only
async def show_statistics(callback: CallbackQuery, session: AsyncSession):
    """Statistikani ko'rsatish"""
    # Statistikani yangilash
    await StatisticsCRUD.update_daily_statistics(session)
    
    # Ma'lumotlarni olish
    total_users = await UserCRUD.get_total_users(session)
    active_today = await UserCRUD.get_active_users_today(session)
    total_downloads = await DownloadCRUD.get_total_downloads(session)
    downloads_today = await DownloadCRUD.get_downloads_today(session)
    format_stats = await DownloadCRUD.get_format_statistics(session)
    
    stats_text = (
        "📊 <b>Bot Statistikasi</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users:,}</b>\n"
        f"✅ Bugun faol: <b>{active_today:,}</b>\n\n"
        f"📥 Jami yuklab olishlar: <b>{total_downloads:,}</b>\n"
        f"📥 Bugun yuklab olishlar: <b>{downloads_today:,}</b>\n\n"
        f"🎥 Video yuklab olishlar: <b>{format_stats['video']:,}</b>\n"
        f"🎵 Audio yuklab olishlar: <b>{format_stats['audio']:,}</b>\n\n"
        f"📅 Oxirgi yangilanish: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=get_admin_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:popular")
@admin_only
async def show_popular_videos(callback: CallbackQuery, session: AsyncSession):
    """Mashhur videolarni ko'rsatish"""
    popular = await DownloadCRUD.get_popular_videos(session, limit=10)
    
    if not popular:
        await callback.answer("Hali ma'lumotlar yo'q", show_alert=True)
        return
    
    text = "🔥 <b>Eng ko'p yuklab olingan videolar:</b>\n\n"
    
    for i, (title, count) in enumerate(popular, 1):
        # Titleni qisqartirish
        short_title = title[:50] + "..." if len(title) > 50 else title
        text += f"{i}. {short_title}\n   📊 {count:,} marta yuklab olindi\n\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_admin_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("admin:ban:"))
@admin_only
async def ban_user_handler(callback: CallbackQuery, session: AsyncSession):
    """Foydalanuvchini bloklash"""
    user_id = int(callback.data.split(":")[2])
    
    success = await UserCRUD.ban_user(session, user_id)
    
    if success:
        await callback.answer(f"✅ Foydalanuvchi {user_id} bloklandi", show_alert=True)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data.startswith("admin:unban:"))
@admin_only
async def unban_user_handler(callback: CallbackQuery, session: AsyncSession):
    """Foydalanuvchi blokini ochish"""
    user_id = int(callback.data.split(":")[2])
    
    success = await UserCRUD.unban_user(session, user_id)
    
    if success:
        await callback.answer(f"✅ Foydalanuvchi {user_id} bloki ochildi", show_alert=True)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "admin:close")
async def close_admin_panel(callback: CallbackQuery):
    """Admin panelni yopish"""
    await callback.message.delete()
    await callback.answer()
