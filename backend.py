from fastapi import FastAPI, APIRouter
from telethon import TelegramClient
import os

app = FastAPI()

# API Router kullanımı
router = APIRouter()

# Telegram API Bilgileri (Çevresel değişkenler)
API_ID = os.getenv("13676960", "")
API_HASH = os.getenv("e7711d9390f24907101c4018011e2da7", "")
PHONE_NUMBER = os.getenv("+905550564025", "")

client = TelegramClient("session_name", API_ID, API_HASH)

@app.on_event("startup")
async def startup_event():
    """FastAPI başlatıldığında Telegram istemcisini başlat."""
    await client.start(PHONE_NUMBER)
    print("✅ Telegram Client Bağlandı!")

@app.on_event("shutdown")
async def shutdown_event():
    """FastAPI kapatılırken Telegram istemcisini kapat."""
    await client.disconnect()
    print("❌ Telegram Client Bağlantısı Kesildi!")

@router.get("/")
async def home():
    return {"message": "FastAPI Backend çalışıyor 🚀"}

@router.get("/get-channels", tags=["channels"])
async def get_channels():
    """Botun katıldığı tüm kanalları listeler ve hata mesajlarını yakalar."""
    try:
        if not client.is_connected():
            await client.connect()

        dialogs = await client.get_dialogs()
        channels = [{"id": d.id, "name": d.title} for d in dialogs if d.is_channel]
        return {"channels": channels}

    except Exception as e:
        print(f"⚠ HATA: {str(e)}")  # Terminalde hatayı göster
        return {"error": str(e)}  # API yanıtında hatayı göster

# API Router'ı FastAPI uygulamasına ekleyelim
app.include_router(router)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render'ın verdiği portu al
    print(f"🚀 Server is running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
