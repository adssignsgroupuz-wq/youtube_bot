from aiogram.types import Message
import asyncio

class ProgressTracker:
    """Yuklanish jarayonini kuzatish"""
    
    def __init__(self, message: Message, total: int):
        self.message = message
        self.total = total
        self.current = 0
        self.last_update = 0
    
    async def update(self, downloaded: int):
        """Progress barni yangilash"""
        self.current = downloaded
        percentage = (downloaded / self.total) * 100
        
        # Har 5% da yangilanadi (spam oldini olish)
        if percentage - self.last_update >= 5:
            self.last_update = percentage
            
            # Progress bar yaratish
            filled = int(percentage / 10)
            bar = "█" * filled + "░" * (10 - filled)
            
            await self.message.edit_text(
                f"⏬ Yuklab olinmoqda...\n\n"
                f"{bar} {percentage:.1f}%\n"
                f"📊 {downloaded / 1024 / 1024:.1f} MB / {self.total / 1024 / 1024:.1f} MB"
            )

class ProgressHook:
    """yt-dlp uchun progress hook"""
    
    def __init__(self, callback):
        self.callback = callback
    
    async def __call__(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            
            if total > 0:
                await self.callback(downloaded, total)
