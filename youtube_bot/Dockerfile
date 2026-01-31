FROM python:3.11-slim

# Ishchi papka yaratish
WORKDIR /app

# System dependencies o'rnatish
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chirish
COPY . .

# Downloads papkasini yaratish
RUN mkdir -p downloads

# Botni ishga tushirish
CMD ["python", "-m", "bot.main"]
