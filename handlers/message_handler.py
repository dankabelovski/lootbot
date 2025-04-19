from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.llm_client import ask_assistant
from services.tool_search import find_tools_by_query
from services.db import get_user_model
from log import logger


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_prompt"):
        from handlers.image import handle_text_for_image
        return await handle_text_for_image(update, context)

    if update.message:
        user_input = update.message.text
        user_id = update.message.from_user.id
    elif update.callback_query and update.callback_query.data.startswith("assistant_reply:"):
        user_input = update.callback_query.data.split(":", 1)[1]
        user_id = update.callback_query.from_user.id
        await update.callback_query.answer()
    else:
        return

    await update.effective_message.chat.send_action("typing")

    try:
        model = get_user_model(user_id)
        reply = await ask_assistant(user_input, model=model)
    except Exception as e:
        logger.error(f"Ошибка при обращении к ассистенту: {e}")
        await update.effective_message.reply_text("⚠️ Не удалось получить ответ.")
        return

    await update.effective_message.reply_text(reply)

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
