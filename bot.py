import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "TU_TOKEN_AQUI"
WEBHOOK_URL = "https://TU_SERVICIO.onrender.com/"  # Reemplaza con la URL pública de tu servicio

# Función de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo ✅")

# Detectar link TikTok
def is_tiktok_url(text):
    return "tiktok.com" in text

# Descargar vídeo TikTok
def download_tiktok(url):
    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "mp4",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

# Handler de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if is_tiktok_url(text):
        await update.message.reply_text("📥 Descargando vídeo...")
        try:
            file_path = download_tiktok(text)
            await update.message.reply_video(video=open(file_path, "rb"))
            os.remove(file_path)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("❌ Envíame un link de TikTok")

# Crear app
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=WEBHOOK_URL
    )
