from typing import Optional
import re

def format_duration(seconds: int) -> str:
    """Sekundlarni soat:daqiqa:soniya formatiga o'tkazish"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"

def format_file_size(size_bytes: int) -> str:
    """Baytlarni MB/GB formatiga o'tkazish"""
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def extract_video_id(url: str) -> Optional[str]:
    """YouTube URL dan video ID ni ajratib olish"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def sanitize_filename(filename: str) -> str:
    """Fayl nomini tozalash (noto'g'ri belgilarni olib tashlash)"""
    # Faqat ruxsat etilgan belgilarni qoldirish
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    # Ko'p bo'sh joylarni bitta bo'sh joyga o'zgartirish
    sanitized = re.sub(r'\s+', ' ', sanitized)
    # Bosh va oxiridagi bo'sh joylarni olib tashlash
    sanitized = sanitized.strip()
    # Maksimal uzunlikni cheklash
    return sanitized[:200]
