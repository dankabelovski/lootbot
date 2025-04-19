from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.llm_client import ask_assistant
from services.tool_matcher import find_tools_by_query
from log import logger

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("awaiting_prompt"):
        from handlers.image import handle_text_for_image
        return await handle_text_for_image(update, context)
    if update.message:
        user_input = update.message.text
    elif update.callback_query and update.callback_query.data.startswith("assistant_reply:"):
        user_input = update.callback_query.data.split(":", 1)[1]
        await update.callback_query.answer()
    else:
        return

    await update.effective_message.chat.send_action("typing")

    try:
        data = await ask_assistant(user_input)
    except Exception as e:
        logger.error(f"Ошибка при обращении к ассистенту: {e}")
        await update.effective_message.reply_text("⚠️ Не удалось получить ответ.")
        return

    reply = data if isinstance(data, str) else "🤖 Что-то пошло не так."
    await update.effective_message.reply_text(reply)

    # Пробуем найти инструменты по ключевым словам
    tools = find_tools_by_query(user_input)

    if tools:
        tool_buttons = [
            [InlineKeyboardButton(name, callback_data=f"tool:{tool_id}:auto")]
            for tool_id, name in tools
        ]
        tool_buttons.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")])

        await update.effective_message.reply_text(
            "💡 Попробуйте эти инструменты:",
            reply_markup=InlineKeyboardMarkup(tool_buttons)
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    print('Это handle_message')
    # Промпт с контекстом
    prompt = f"Ты — ассистент Telegram-бота с инструментами. Пользователь спрашивает: {user_text}. Дай полезный, краткий ответ и предложи инструменты, если подходят."

    response = await ask_assistant(prompt, model="mixtral")  # или mistral:7b-instruct
    await context.bot.send_message(chat_id=chat_id, text=response)