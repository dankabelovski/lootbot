import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from log import logger

# Старт и помощь
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.admin import reload_handler
from handlers.tools import back_to_main_callback

# Промпты
from handlers.prompt import prompt_handler, prompt_callback
from handlers.prompt_custom import (
    prompt_custom_start,
    prompt_param_select,
    prompt_set_param,
    prompt_generate,
    prompt_param_back
)

# Инструменты
from handlers.tools import (
    tools_handler,
    tools_callback,
    tool_detail_callback,
    tool_scenarios_callback,
    tools_back_callback,
    back_to_category_callback
)

# Статьи (insights)
from handlers.insights import (
    insights_handler,
    articles_by_category,
    article_detail,
    back_to_articles_callback
)

# Ассистент и профиль
from handlers.assistant_mode import go_assistant, assistant_button_reply
from handlers.message_handler import message_handler
from handlers.profile import profile_handler, set_model_callback
from handlers.image import image_command, image_model_select

async def error_handler(update, context):
    logger.error(f"Ошибка: {context.error}")

# Загрузка токена
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Навигационные команды
async def go_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await help_handler(update, context)

async def go_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await prompt_handler(update, context)

async def go_prompt_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await prompt_custom_start(update, context)

async def go_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await tools_handler(update, context)

async def go_insights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await insights_handler(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("prompt", prompt_handler))
    app.add_handler(CommandHandler("insights", insights_handler))
    app.add_handler(CommandHandler("tools", tools_handler))
    app.add_handler(CommandHandler("prompt_custom", prompt_custom_start))
    app.add_handler(CommandHandler("reload", reload_handler))
    app.add_handler(CommandHandler("image", image_command))
    app.add_handler(CommandHandler("profile", profile_handler))

    # Промпты
    app.add_handler(CallbackQueryHandler(prompt_callback, pattern="^(MidJourney|DALL·E|Stable Diffusion)$"))
    app.add_handler(CallbackQueryHandler(prompt_param_select, pattern="^param:"))
    app.add_handler(CallbackQueryHandler(prompt_set_param, pattern="^set:"))
    app.add_handler(CallbackQueryHandler(prompt_generate, pattern="^generate_prompt_custom$"))
    app.add_handler(CallbackQueryHandler(prompt_param_back, pattern="^prompt_custom_back$"))

    # Навигация
    app.add_handler(CallbackQueryHandler(back_to_main_callback, pattern="^back_to_main$"))
    app.add_handler(CallbackQueryHandler(go_prompt, pattern="^go_prompt$"))
    app.add_handler(CallbackQueryHandler(go_prompt_custom, pattern="^go_prompt_custom$"))
    app.add_handler(CallbackQueryHandler(go_tools, pattern="^go_tools$"))
    app.add_handler(CallbackQueryHandler(go_insights, pattern="^go_insights$"))
    app.add_handler(CallbackQueryHandler(go_help, pattern="^go_help$"))

    # Инструменты
    app.add_handler(CallbackQueryHandler(tools_callback, pattern="^tools:"))
    app.add_handler(CallbackQueryHandler(tool_detail_callback, pattern="^tool:"))
    app.add_handler(CallbackQueryHandler(tool_scenarios_callback, pattern="^scenarios:"))
    app.add_handler(CallbackQueryHandler(tools_back_callback, pattern="^go_tools$"))
    app.add_handler(CallbackQueryHandler(back_to_category_callback, pattern="^back_to_category:"))

    # Статьи
    app.add_handler(CallbackQueryHandler(insights_handler, pattern="^go_insights$"))
    app.add_handler(CallbackQueryHandler(articles_by_category, pattern="^articles:"))
    app.add_handler(CallbackQueryHandler(article_detail, pattern="^article:"))
    app.add_handler(CallbackQueryHandler(back_to_articles_callback, pattern="^back_to_articles$"))

    # Ассистент и профиль
    app.add_handler(CallbackQueryHandler(go_assistant, pattern="^go_assistant$"))
    app.add_handler(CallbackQueryHandler(assistant_button_reply, pattern="^assistant_reply:"))
    app.add_handler(CallbackQueryHandler(set_model_callback, pattern="^set_model:"))

    # Модель изображения
    app.add_handler(CallbackQueryHandler(image_model_select, pattern="^image_model:"))

    # Обработка всех текстов (ассистент, генерация, предложения)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.add_error_handler(error_handler)

    print("Бот запущен...")
    app.run_polling()
