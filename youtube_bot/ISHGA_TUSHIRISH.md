# 🚀 ISHGA TUSHIRISH QO'LLANMASI

## 📋 Talablar

- Python 3.9 yoki yuqori
- pip (Python package manager)
- FFmpeg (audio konvertatsiya uchun)

## 🔧 Bosqichma-bosqich o'rnatish

### 1-QADAM: Python versiyasini tekshirish
```bash
python --version
# yoki
python3 --version
```

Agar Python o'rnatilmagan bo'lsa: https://www.python.org/downloads/

### 2-QADAM: FFmpeg o'rnatish

**Windows:**
1. https://ffmpeg.org/download.html ga o'ting
2. FFmpeg yuklab oling
3. PATH ga qo'shing

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 3-QADAM: Loyiha papkasiga o'tish
```bash
cd youtube_bot
```

### 4-QADAM: Virtual environment yaratish
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 5-QADAM: Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 6-QADAM: Bot yaratish (BotFather)

1. Telegram'da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` komandasini yuboring
3. Bot nomini kiriting (misol: `My YouTube Bot`)
4. Bot username kiriting (misol: `my_youtube_bot`)
5. Token ni nusxalang

### 7-QADAM: Admin ID topish

1. Telegram'da [@userinfobot](https://t.me/userinfobot) ga o'ting
2. `/start` bosing
3. Sizning ID raqamingizni nusxalang

### 8-QADAM: .env faylini yaratish

`.env.example` faylini `.env` ga nusxalang:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

`.env` faylini tahrirlang:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # BotFather dan olgan token
ADMIN_IDS=123456789                               # Sizning Telegram ID
DATABASE_URL=sqlite+aiosqlite:///bot.db
MAX_FILE_SIZE=2147483648
```

### 9-QADAM: Botni ishga tushirish
```bash
python -m bot.main
```

Agar hammasi to'g'ri bo'lsa, quyidagi xabar ko'rinadi:
```
INFO - Database muvaffaqiyatli ishga tushdi!
INFO - Bot ishga tushdi!
```

## ✅ Botni sinash

1. Telegram'da botingizni toping
2. `/start` ni bosing
3. YouTube video linkini yuboring
4. Format va sifatni tanlang
5. Video yuklab olinishini kuting!

## 🛑 Botni to'xtatish

Terminelda `Ctrl + C` bosing

## 🐳 Docker bilan ishga tushirish (qo'shimcha)

Agar Docker o'rnatilgan bo'lsa:

```bash
# Build
docker-compose build

# Ishga tushirish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f

# To'xtatish
docker-compose down
```

## ❓ Muammolar va yechimlar

### 1. "ModuleNotFoundError: No module named 'aiogram'"
**Yechim:** Kutubxonalarni qayta o'rnating:
```bash
pip install -r requirements.txt
```

### 2. "FFmpeg not found"
**Yechim:** FFmpeg o'rnatilganligini tekshiring:
```bash
ffmpeg -version
```

### 3. "Invalid bot token"
**Yechim:** `.env` faylidagi BOT_TOKEN ni tekshiring

### 4. "Database error"
**Yechim:** `bot.db` faylini o'chirib, qayta ishga tushiring

## 📞 Yordam

Agar muammo hal bo'lmasa:
- README.md faylini o'qing
- GitHub Issues bo'limida savol bering
- Telegram: @yoursupport

---

**Omad! 🚀**
