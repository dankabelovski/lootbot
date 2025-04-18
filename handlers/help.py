from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.context_helpers import get_effective_message


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_effective_message(update)

    text = (
        "🧭 *Добро пожаловать в Loot & Learn!*\n\n"
        "Этот бот — твой спутник в мире AI, автоматизации и цифровой алхимии.\n\n"
        "*Вот как ты можешь использовать его на максимум:*\n\n"
        "🎯 /prompt — Получи готовый промпт для MidJourney, DALL·E или SD\n"
        "🎛 /prompt_custom — Собери свой промпт по параметрам: стиль, сцена, атмосфера\n"
        "🧰 /tools — Открой базу AI-инструментов с постами и сценариями\n"
        "🧠 /insights — Читай статьи, которые раскрывают суть ИИ и автоматизации\n\n"
        "💡 *Советы:*\n"
        "— Используй /start для быстрого доступа к разделам\n"
        "— Загляни в [наш канал](https://t.me/loot_and_learn) — там ещё больше\n"
        "— В будущем появятся ⭐ звезды, донаты и AI-ассистент\n\n"
        "Пользуйся ботом как творческой лабораторией.\n"
        "Я рядом, чтобы сделать это удобным 💎"
    )

    keyboard = [
        [InlineKeyboardButton("🎯 Быстрый промпт", callback_data="go_prompt")],
        [InlineKeyboardButton("🎛 Генератор промпта", callback_data="go_prompt_custom")],
        [InlineKeyboardButton("🧰 Инструменты", callback_data="go_tools")],
        [InlineKeyboardButton("🧠 Полезные статьи", callback_data="go_insights")]
    ]

    await message.reply_text(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
