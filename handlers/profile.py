# handlers/profile.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.users import get_user_model
from services.db import set_user_model


async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id
    current_model = get_user_model(telegram_id)

    display_model = {
        "mistralai/mistral-7b-instruct": "🐦 Mistral (от Mistral AI, Франция)",
        "cohere/command-r-plus": "⚖️ Command R+ (от Cohere, Канада)",
        "anthropic/claude-3-opus": "🧠 Claude 3 (от Anthropic, США)"
    }.get(current_model, current_model)

    text = (
        f"👤 *Профиль*\n\n"
        f"Выбранная языковая модель: `{display_model}`\n\n"
        "Выберите ИИ-модель для ассистента:"
    )

    keyboard = [
        [InlineKeyboardButton("🐦 Mistral (от Mistral AI)", callback_data="set_model:mistralai/mistral-7b-instruct")],
        [InlineKeyboardButton("⚖️ Command R+ (от Cohere)", callback_data="set_model:cohere/command-r-plus")],
        [InlineKeyboardButton("🧠 Claude 3 (от Anthropic)", callback_data="set_model:anthropic/claude-3-sonnet")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
    ]

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def set_model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    model = query.data.split(":")[1]
    telegram_id = query.from_user.id

    set_user_model(telegram_id, model)  # Сохраняем в БД
    context.user_data["llm_model"] = model  # Сохраняем в сессии

    await query.edit_message_text(
        f"✅ Модель обновлена!\n\nТеперь используется:\n`{model}`",
        parse_mode="Markdown"
    )
