from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.huggingface_client import generate_image, MODELS
from log import logger


# Шаг 1: /image — выбор модели
async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"image_model:{name}")]
        for name in MODELS.keys()
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎨 Выбери модель генерации изображения:",
        reply_markup=markup
    )


# Шаг 2: сохранение модели и запрос описания
async def image_model_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    model_name = query.data.split(":", 1)[1]
    model_url = MODELS.get(model_name)

    if not model_url:
        await query.edit_message_text("❌ Модель не найдена.")
        return

    context.user_data["image_model_url"] = model_url
    context.user_data["awaiting_prompt"] = True

    await query.edit_message_text("✏️ Введи описание изображения для генерации:")


# Шаг 3: генерация изображения
async def handle_text_for_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_prompt"):
        return

    prompt = update.message.text
    model_url = context.user_data.get("image_model_url")

    if not model_url:
        await update.message.reply_text("❌ Модель не выбрана.")
        return

    await update.message.reply_text("🧠 Генерирую изображение, подожди немного...")

    try:
        image_bytes = generate_image(prompt, model_url)
        await update.message.reply_photo(photo=image_bytes)
    except Exception as e:
        logger.error(f"Ошибка генерации: {e}")
        await update.message.reply_text(f"❌ Ошибка генерации: {e}")

    context.user_data["awaiting_prompt"] = False
