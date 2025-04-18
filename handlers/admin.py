from telegram import Update
from telegram.ext import ContextTypes
from services.cache import reload_cache

async def reload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reload_cache()
    await update.message.reply_text("♻️ Кэш обновлён!")
