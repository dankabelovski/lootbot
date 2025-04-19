from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from log import logger
from services.tool_matcher import find_tools_by_query
from db.users import upsert_user, get_user_model
from services.llm_client import ask_assistant


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Сохраняем или обновляем пользователя в базе
    upsert_user(user.id, user.username)

    # Получаем выбранную модель пользователя
    model_name = get_user_model(user.id)

    # Определяем текст запроса
    if update.message:
        user_input = update.message.text
    elif update.callback_query and update.callback_query.data.startswith("assistant_reply:"):
        user_input = update.callback_query.data.split(":", 1)[1]
        await update.callback_query.answer()
    else:
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Формируем промпт
    prompt = f"Ты — ассистент Telegram-бота. Пользователь спрашивает: {user_input}. Ответь полезно и кратко. Если есть подходящие инструменты, предложи их."

    try:
        response = await ask_assistant(prompt, model=model_name)
    except Exception as e:
        logger.error(f"Ошибка ассистента: {e}")
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Не удалось получить ответ от ассистента.")
        return

    reply_text = response if isinstance(response, str) else response.get("reply", "🤖 Что-то пошло не так.")
    await context.bot.send_message(chat_id=chat_id, text=reply_text)

    # Поиск инструментов по запросу
    tools = find_tools_by_query(user_input)

    if tools:
        tool_buttons = [
            [InlineKeyboardButton(name, callback_data=f"tool:{tool_id}:auto")]
            for tool_id, name in tools
        ]
        tool_buttons.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")])

        await context.bot.send_message(
            chat_id=chat_id,
            text="💡 Попробуйте эти инструменты:",
            reply_markup=InlineKeyboardMarkup(tool_buttons)
        )
