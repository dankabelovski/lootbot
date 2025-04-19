from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.llm_client import ask_assistant
from services.tool_matcher import find_tools_by_query
from services.article_search import find_articles_by_query
from log import logger
from db.users import get_user_model

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id



    # Шаг 1. Краткий ответ от ассистента
    prompt = (
        f"Ты — ассистент Telegram-бота с инструментами и статьями."
        f" Пользователь спрашивает: '{user_input}'."
        f" Ответь кратко (2-3 предложения) и если есть подходящие инструменты или статьи, упомяни, что они найдены."
    )

    try:
        short_reply = await ask_assistant(prompt, model=context.user_data.get("llm_model"))
    except Exception as e:
        logger.error(f"Ошибка при получении краткого ответа от ассистента: {e}")
        await update.message.reply_text("⚠️ Не удалось получить ответ от ассистента.")
        return

    await update.message.reply_text(short_reply)

    # Шаг 2. Поиск подходящих инструментов
    tools = find_tools_by_query(user_input)
    articles = find_articles_by_query(user_input)

    buttons = []

    if tools:
        for tool_id, name in tools:
            buttons.append([InlineKeyboardButton(f"🛠 {name}", callback_data=f"tool:{tool_id}:auto")])

    if articles:
        for article_id, title in articles:
            buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f"article:{article_id}")])

    if tools or articles:
        buttons.append([InlineKeyboardButton("📖 Рассказать подробнее", callback_data=f"assistant_reply:{user_input}")])
        buttons.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")])
        await update.message.reply_text(
            "Вот что я нашёл по твоему запросу:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        # Если ничего не найдено, просто предложить узнать подробнее
        await update.message.reply_text(
            "📌 Хочешь узнать больше?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📖 Рассказать подробнее", callback_data=f"assistant_reply:{user_input}")],
                [InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")]
            ])
        )


async def assistant_explain_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_input = query.data.split(":", 1)[1]

    prompt = f"Пользователь спрашивает: {user_input}. Дай полный и полезный ответ, как эксперт по ИИ-инструментам."
    try:
        response = await ask_assistant(prompt)
        await query.message.reply_text(response)
    except Exception as e:
        logger.error(f"Ошибка пояснения: {e}")
        await query.message.reply_text("⚠️ Не удалось получить пояснение.")
