from datetime import datetime
from sqlalchemy import BigInteger, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional

class Base(DeclarativeBase):
    """Asosiy model"""
    pass

class User(Base):
    """Foydalanuvchi modeli"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram user ID
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    downloads: Mapped[list["Download"]] = relationship(back_populates="user")
    
    def __repr__(self):
        return f"<User {self.id} - {self.username}>"

class Download(Base):
    """Yuklab olingan videolar statistikasi"""
    __tablename__ = "downloads"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    video_id: Mapped[str] = mapped_column(String(50))
    video_title: Mapped[str] = mapped_column(String(500))
    video_url: Mapped[str] = mapped_column(String(500))
    format_type: Mapped[str] = mapped_column(String(20))  # video/audio
    quality: Mapped[str] = mapped_column(String(20))
    file_size: Mapped[int] = mapped_column(BigInteger)  # bytes
    duration: Mapped[int] = mapped_column(Integer)  # seconds
    is_playlist: Mapped[bool] = mapped_column(Boolean, default=False)
    downloaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user: Mapped["User"] = relationship(back_populates="downloads")
    
    def __repr__(self):
        return f"<Download {self.video_id} by User {self.user_id}>"

class Statistics(Base):
    """Umumiy statistika"""
    __tablename__ = "statistics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total_users: Mapped[int] = mapped_column(Integer, default=0)
    active_users_today: Mapped[int] = mapped_column(Integer, default=0)
    total_downloads: Mapped[int] = mapped_column(Integer, default=0)
    downloads_today: Mapped[int] = mapped_column(Integer, default=0)
    video_downloads: Mapped[int] = mapped_column(Integer, default=0)
    audio_downloads: Mapped[int] = mapped_column(Integer, default=0)
    
    def __repr__(self):
        return f"<Statistics {self.date}>"
