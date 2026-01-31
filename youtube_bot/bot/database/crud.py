from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional, List
from bot.database.models import User, Download, Statistics

class UserCRUD:
    """User operatsiyalari"""
    
    @staticmethod
    async def get_or_create_user(
        session: AsyncSession,
        user_id: int,
        username: Optional[str],
        full_name: str
    ) -> User:
        """Foydalanuvchini olish yoki yaratish"""
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                id=user_id,
                username=username,
                full_name=full_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            # Oxirgi faollik vaqtini yangilash
            user.last_activity = datetime.utcnow()
            if username:
                user.username = username
            user.full_name = full_name
            await session.commit()
        
        return user
    
    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
        """Foydalanuvchini olish"""
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def ban_user(session: AsyncSession, user_id: int) -> bool:
        """Foydalanuvchini bloklash"""
        user = await UserCRUD.get_user(session, user_id)
        if user:
            user.is_banned = True
            await session.commit()
            return True
        return False
    
    @staticmethod
    async def unban_user(session: AsyncSession, user_id: int) -> bool:
        """Foydalanuvchi blokini ochish"""
        user = await UserCRUD.get_user(session, user_id)
        if user:
            user.is_banned = False
            await session.commit()
            return True
        return False
    
    @staticmethod
    async def is_user_banned(session: AsyncSession, user_id: int) -> bool:
        """Foydalanuvchi bloklangan yoki yo'qligini tekshirish"""
        user = await UserCRUD.get_user(session, user_id)
        return user.is_banned if user else False
    
    @staticmethod
    async def get_total_users(session: AsyncSession) -> int:
        """Jami foydalanuvchilar soni"""
        result = await session.execute(select(func.count(User.id)))
        return result.scalar_one()
    
    @staticmethod
    async def get_active_users_today(session: AsyncSession) -> int:
        """Bugun faol foydalanuvchilar soni"""
        today = datetime.utcnow().date()
        result = await session.execute(
            select(func.count(User.id)).where(
                func.date(User.last_activity) == today
            )
        )
        return result.scalar_one()

class DownloadCRUD:
    """Download operatsiyalari"""
    
    @staticmethod
    async def create_download(
        session: AsyncSession,
        user_id: int,
        video_id: str,
        video_title: str,
        video_url: str,
        format_type: str,
        quality: str,
        file_size: int,
        duration: int,
        is_playlist: bool = False
    ) -> Download:
        """Yuklab olish yozuvini yaratish"""
        download = Download(
            user_id=user_id,
            video_id=video_id,
            video_title=video_title,
            video_url=video_url,
            format_type=format_type,
            quality=quality,
            file_size=file_size,
            duration=duration,
            is_playlist=is_playlist
        )
        session.add(download)
        await session.commit()
        await session.refresh(download)
        return download
    
    @staticmethod
    async def get_user_downloads(
        session: AsyncSession,
        user_id: int,
        limit: int = 10
    ) -> List[Download]:
        """Foydalanuvchining yuklab olishlari"""
        result = await session.execute(
            select(Download)
            .where(Download.user_id == user_id)
            .order_by(desc(Download.downloaded_at))
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_total_downloads(session: AsyncSession) -> int:
        """Jami yuklab olishlar soni"""
        result = await session.execute(select(func.count(Download.id)))
        return result.scalar_one()
    
    @staticmethod
    async def get_downloads_today(session: AsyncSession) -> int:
        """Bugun yuklab olishlar soni"""
        today = datetime.utcnow().date()
        result = await session.execute(
            select(func.count(Download.id)).where(
                func.date(Download.downloaded_at) == today
            )
        )
        return result.scalar_one()
    
    @staticmethod
    async def get_popular_videos(
        session: AsyncSession,
        limit: int = 10
    ) -> List[tuple]:
        """Eng ko'p yuklab olingan videolar"""
        result = await session.execute(
            select(
                Download.video_title,
                func.count(Download.id).label('download_count')
            )
            .group_by(Download.video_title)
            .order_by(desc('download_count'))
            .limit(limit)
        )
        return list(result.all())
    
    @staticmethod
    async def get_format_statistics(session: AsyncSession) -> dict:
        """Format bo'yicha statistika"""
        result = await session.execute(
            select(
                Download.format_type,
                func.count(Download.id).label('count')
            )
            .group_by(Download.format_type)
        )
        stats = {row.format_type: row.count for row in result.all()}
        return {
            'video': stats.get('video', 0),
            'audio': stats.get('audio', 0)
        }

class StatisticsCRUD:
    """Statistika operatsiyalari"""
    
    @staticmethod
    async def update_daily_statistics(session: AsyncSession):
        """Kunlik statistikani yangilash"""
        today = datetime.utcnow().date()
        
        # Bugungi statistikani topish yoki yaratish
        result = await session.execute(
            select(Statistics).where(func.date(Statistics.date) == today)
        )
        stat = result.scalar_one_or_none()
        
        if not stat:
            stat = Statistics(date=datetime.utcnow())
            session.add(stat)
        
        # Yangi qiymatlarni hisoblash
        stat.total_users = await UserCRUD.get_total_users(session)
        stat.active_users_today = await UserCRUD.get_active_users_today(session)
        stat.total_downloads = await DownloadCRUD.get_total_downloads(session)
        stat.downloads_today = await DownloadCRUD.get_downloads_today(session)
        
        format_stats = await DownloadCRUD.get_format_statistics(session)
        stat.video_downloads = format_stats['video']
        stat.audio_downloads = format_stats['audio']
        
        await session.commit()
        return stat
