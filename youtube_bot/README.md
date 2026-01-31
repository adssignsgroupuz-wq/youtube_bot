# 🎥 YouTube Downloader Bot

Professional YouTube video va audio yuklab olish Telegram boti.

## 🌟 Xususiyatlar

- ✅ **Video yuklab olish** - 1080p, 720p, 480p, 360p sifatlarda
- ✅ **Audio yuklab olish** - MP3 formatda (320kbps, 192kbps, 128kbps)
- ✅ **Playlist support** - Butun playlistni yuklab olish
- ✅ **Database** - Statistika va foydalanuvchilar bazasi
- ✅ **Admin Panel** - To'liq boshqaruv paneli
- ✅ **Rate Limiting** - Spam himoyasi
- ✅ **Ban System** - Foydalanuvchilarni bloklash
- ✅ **Progress Bar** - Yuklanish jarayonini ko'rsatish

## 📦 O'rnatish

### 1. Repository ni klonlash
```bash
git clone <repository_url>
cd youtube_bot
```

### 2. Virtual environment yaratish
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash
```bash
cp .env.example .env
nano .env
```

`.env` fayliga quyidagilarni kiriting:
```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=your_telegram_id,another_admin_id
DATABASE_URL=sqlite+aiosqlite:///bot.db
MAX_FILE_SIZE=2147483648
```

### 5. Botni ishga tushirish
```bash
python -m bot.main
```

## 🔧 Konfiguratsiya

### Bot Token olish
1. Telegram'da [@BotFather](https://t.me/BotFather) ga boring
2. `/newbot` komandasini yuboring
3. Bot nomini va username ni kiriting
4. Token ni `.env` fayliga qo'shing

### Admin ID topish
1. Telegram'da [@userinfobot](https://t.me/userinfobot) ga boring
2. Botga `/start` yuboring
3. Sizning ID ni ko'rsatadi
4. ID ni `.env` fayliga qo'shing

## 📊 Database

Bot SQLite yoki PostgreSQL ishlatadi. Default SQLite.

PostgreSQL ishlatish uchun:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

## 🎮 Foydalanish

### Oddiy foydalanuvchilar uchun:
1. Botga `/start` yuboring
2. YouTube video linkini yuboring
3. Format tanlang (Video/Audio)
4. Sifatni tanlang
5. Yuklanishni kuting!

### Admin uchun:
- `/admin` - Admin panel
- Statistika ko'rish
- Mashhur videolarni ko'rish
- Foydalanuvchilarni bloklash/ochish

## 🐳 Docker bilan ishga tushirish

```bash
docker build -t youtube_bot .
docker run -d --name youtube_bot --env-file .env youtube_bot
```

## 📝 Loyiha strukturasi

```
youtube_bot/
├── bot/
│   ├── config.py          # Konfiguratsiya
│   ├── main.py            # Asosiy fayl
│   ├── handlers/          # Handlerlar
│   ├── keyboards/         # Klaviaturalar
│   ├── middlewares/       # Middlewarelar
│   ├── services/          # Xizmatlar
│   ├── database/          # Database modellari
│   └── utils/             # Yordamchi funksiyalar
├── downloads/             # Vaqtinchalik fayllar
├── requirements.txt       # Kutubxonalar
└── .env.example          # Konfiguratsiya namunasi
```

## 🛡️ Xavfsizlik

- ❌ Hech qachon `.env` faylini GitHub'ga yuklamang
- ✅ `.gitignore` da `.env` mavjudligini tekshiring
- ✅ Admin ID larni to'g'ri kiriting
- ✅ Database ma'lumotlarini himoyalang

## 🤝 Hissa qo'shish

Pull request'lar qabul qilinadi!

## 📄 Litsenziya

MIT License

## 📞 Aloqa

Savollar bo'lsa: @yoursupport

---

**Made with ❤️ by Your Name**
