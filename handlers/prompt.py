# handlers/prompt.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.context_helpers import get_effective_message


async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_effective_message(update)

    keyboard = [
        [InlineKeyboardButton("MidJourney", callback_data="MidJourney")],
        [InlineKeyboardButton("DALL·E", callback_data="DALL·E")],
        [InlineKeyboardButton("Stable Diffusion", callback_data="Stable Diffusion")]
    ]

    await message.reply_text(
        "Выбери платформу для генерации промпта:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def prompt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    platform = query.data
    examples = {
        "MidJourney": "cyberpunk robot, neon lights, ultra-detailed --v 5 --ar 16:9",
        "DALL·E": "a futuristic city floating in the clouds, digital art",
        "Stable Diffusion": "portrait of a fantasy elf warrior, realistic, 4k"
    }

    prompt = examples.get(platform, "Платформа не найдена.")
    await query.edit_message_text(f"🧠 *Промпт для {platform}:*\n\n`{prompt}`", parse_mode="Markdown")
