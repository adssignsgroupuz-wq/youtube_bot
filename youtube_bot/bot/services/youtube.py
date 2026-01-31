import yt_dlp
import os
from typing import Dict, Optional
from bot.config import config

class YouTubeService:
    """YouTube video yuklab olish xizmati"""
    
    @staticmethod
    async def get_video_info(url: str) -> Optional[Dict]:
        """Video haqida ma'lumot olish"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'id': info['id'],
                    'title': info['title'],
                    'duration': info['duration'],
                    'thumbnail': info['thumbnail'],
                    'uploader': info['uploader'],
                    'view_count': info.get('view_count', 0)
                }
        except Exception as e:
            print(f"Video ma'lumotlarini olishda xatolik: {e}")
            return None
    
    @staticmethod
    async def download_video(video_id: str, quality: str, output_path: str) -> Optional[str]:
        """Video yuklab olish"""
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': True,
        }
        
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return output_path
        except Exception as e:
            print(f"Video yuklab olishda xatolik: {e}")
            return None
    
    @staticmethod
    async def download_audio(video_id: str, quality: str, output_path: str) -> Optional[str]:
        """Audio yuklab olish"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'quiet': False,
            'no_warnings': True,
        }
        
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            # MP3 fayl nomi .mp3 extension bilan yaratiladi
            mp3_path = output_path.rsplit('.', 1)[0] + '.mp3'
            return mp3_path
        except Exception as e:
            print(f"Audio yuklab olishda xatolik: {e}")
            return None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """URL tekshirish"""
        youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com']
        return any(domain in url for domain in youtube_domains)
    
    @staticmethod
    async def get_playlist_info(url: str) -> Optional[Dict]:
        """Playlist ma'lumotlarini olish"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' not in info:
                    return None
                
                videos = []
                for entry in info['entries']:
                    if entry:
                        videos.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'url': f"https://www.youtube.com/watch?v={entry.get('id')}"
                        })
                
                return {
                    'title': info.get('title', 'Playlist'),
                    'videos': videos
                }
        except Exception as e:
            print(f"Playlist ma'lumotlarini olishda xatolik: {e}")
            return None
