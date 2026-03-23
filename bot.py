import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "tiktok.com" in text:
        await update.message.reply_text("✅ Video recibido. Procesando en breve...")
    else:
        await update.message.reply_text("❌ Envíame un enlace de TikTok válido.")

app = ApplicationBuilder().token("8747109864:AAH5lrmXS10Rjyi5dy5aB_Ss9Fs8FtSdE4M").build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
