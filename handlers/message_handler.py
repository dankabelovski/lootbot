from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.llm_client import ask_assistant
from services.tool_matcher import find_tools_by_query
from services.article_search import find_articles_by_query
from log import logger
from db.users import get_user_model
from services.prompt_templates import CLAUDE_PROMPT_TEMPLATE, MISTRAL_PROMPT_TEMPLATE
from db.tags import get_all_tags


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id

    # Получаем модель пользователя
    model = context.user_data.get("llm_model")
    if not model:
        model = get_user_model(chat_id)
        context.user_data["llm_model"] = model

    # История сообщений для контекста
    history = context.user_data.get("chat_history", [])
    history.append({"role": "user", "content": user_input})

    # Шаблон промпта
    if "claude" in model:
        system_prompt = CLAUDE_PROMPT_TEMPLATE.format(user_input=user_input)
    else:
        system_prompt = MISTRAL_PROMPT_TEMPLATE.format(user_input=user_input)

    # Создаем полное тело запроса
    prompt_messages = [{"role": "system", "content": system_prompt}] + history[-5:]  # максимум 5 последних реплик

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    try:
        short_reply = await ask_assistant(prompt_messages, model=model)
    except Exception as e:
        logger.error(f"Ошибка при получении краткого ответа от ассистента: {e}")
        await update.message.reply_text("⚠️ Не удалось получить ответ от ассистента.")
        return

    await update.message.reply_text(short_reply)

    # Сохраняем ответ ассистента в историю
    history.append({"role": "assistant", "content": short_reply})
    context.user_data["chat_history"] = history
    context.user_data["last_query"] = user_input

    # Поиск инструментов и статей
    tools = find_tools_by_query(user_input)
    articles = find_articles_by_query(user_input)

    buttons = []
    if tools:
        for tool_id, name in tools:
            buttons.append([InlineKeyboardButton(f"🛠 {name}", callback_data=f"tool:{tool_id}:auto")])

    if articles:
        for article_id, short_title in articles:
            buttons.append([InlineKeyboardButton(f"📚 {short_title}", callback_data=f"article:{article_id}")])

    if tools or articles:
        buttons.append([InlineKeyboardButton("📖 Рассказать подробнее", callback_data="assistant_reply")])

    buttons.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")])

    await update.message.reply_text(
        "Вот что я нашёл по твоему запросу:" if tools or articles else "📌 Хочешь узнать больше?",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def assistant_explain_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_input = context.user_data.get("last_query", "")
    if not user_input:
        await query.message.reply_text("⚠️ Не найден последний запрос.")
        return

    model = context.user_data.get("llm_model")
    if not model:
        model = get_user_model(query.from_user.id)

    history = context.user_data.get("chat_history", [])
    history.append({"role": "user", "content": user_input})

    prompt = "Дай подробный, экспертный ответ по теме, включая пояснение и рекомендации."
    full_prompt = [{"role": "system", "content": prompt}] + history[-5:]

    await context.bot.send_chat_action(chat_id=query.message.chat.id, action="typing")
    try:
        response = await ask_assistant(full_prompt, model=model)
        history.append({"role": "assistant", "content": response})
        context.user_data["chat_history"] = history
        await query.message.reply_text(response)
    except Exception as e:
        logger.error(f"Ошибка пояснения: {e}")
        await query.message.reply_text("⚠️ Не удалось получить пояснение.")
