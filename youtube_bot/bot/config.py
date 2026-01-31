import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Config:
    """Bot konfiguratsiyasi"""
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    ADMIN_IDS: list[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 2147483648))  # 2GB
    DOWNLOADS_DIR: str = "downloads"

config = Config()

# Downloads papkasini yaratish
os.makedirs(config.DOWNLOADS_DIR, exist_ok=True)
