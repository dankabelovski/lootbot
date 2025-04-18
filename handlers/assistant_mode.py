from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from handlers.message_handler import message_handler

async def go_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["mode"] = "assistant"

    keyboard = [[InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")]]

    await query.edit_message_text(
        "🧠 Я ассистент. Напиши мне любой вопрос — я постараюсь помочь!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def assistant_button_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await message_handler(update, context)