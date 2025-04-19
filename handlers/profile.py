from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.db import set_user_model

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🐦 Mistral", callback_data="set_model:mistralai/mistral-7b-instruct")],
        [InlineKeyboardButton("⚖️ Command R+", callback_data="set_model:cohere/command-r-plus")],
        [InlineKeyboardButton("🧠 Claude 3", callback_data="set_model:anthropic/claude-3-sonnet")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧠 Выберите модель ИИ:", reply_markup=markup)

async def set_model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    model_id = query.data.split(":", 1)[1]
    user_id = update.effective_user.id

    set_user_model(user_id, model_id)

    await query.edit_message_text(
        f"✅ Модель обновлена!\n\nТеперь используется:\n`{model_id}`",
        parse_mode="Markdown"
    )
