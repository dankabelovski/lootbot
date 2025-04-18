from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from log import logger
from utils.context_helpers import get_effective_message


# Шаг 1 — старт команды
async def prompt_custom_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    default_values = {
        "style": "реализм",
        "scene": "город",
        "atmo": "яркая",
        "format": "обложка"
    }
    context.user_data.update(default_values)

    message = get_effective_message(update)
    await show_prompt_menu(message, context)

    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("\U0001F3A8 Стиль", callback_data="param:style")],
        [InlineKeyboardButton("\U0001F3DE Сцена", callback_data="param:scene")],
        [InlineKeyboardButton("\U0001F4A1 Атмосфера", callback_data="param:atmo")],
        [InlineKeyboardButton("\U0001F4D0 Формат", callback_data="param:format")],
        [InlineKeyboardButton("\U0001F3AF Сгенерировать промпт", callback_data="generate_prompt_custom")]
    ]
    await update.message.reply_text("Выбери параметры:", reply_markup=InlineKeyboardMarkup(keyboard))


# Шаг 2 — выбор конкретного значения параметра
async def prompt_param_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    param_type = query.data.split(":")[1]
    options = {
        "style": ["аниме", "реализм", "пиксель-арт"],
        "scene": ["город", "лес", "космос"],
        "atmo": ["мрачная", "яркая", "ретро"],
        "format": ["портрет", "обложка", "сцена"]
    }

    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"set:{param_type}:{opt}")]
        for opt in options[param_type]
    ]
    buttons.append([InlineKeyboardButton("\u2B05 Назад", callback_data="prompt_custom_back")])

    await query.edit_message_text(
        f"Выбери значение для: *{param_type}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Шаг 3 — установка выбранного значения
async def prompt_set_param(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, param_type, value = query.data.split(":")
    context.user_data[param_type] = value
    logger.info(f"[PROMPT] {param_type} = {value}")

    await show_prompt_menu(query, context)


# Шаг 4 — генерация финального промпта
async def prompt_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    style = context.user_data.get("style", "стиль не выбран")
    scene = context.user_data.get("scene", "сцена не выбрана")
    atmo = context.user_data.get("atmo", "атмосфера не выбрана")
    format_ = context.user_data.get("format", "формат не выбран")

    prompt = f"Изображение в стиле {style}, сцена — {scene}, атмосфера — {atmo}, формат — {format_}."

    await query.edit_message_text(
        text=f"\U0001F9E0 *Готовый промпт:*\n\n`{prompt}`",
        parse_mode="Markdown"
    )


async def show_prompt_menu(update_or_message, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data

    text = (
        "\U0001F39B *Выбранные параметры:*\n\n"
        f"\U0001F3A8 Стиль: {data.get('style')}\n"
        f"\U0001F3DE Сцена: {data.get('scene')}\n"
        f"\U0001F4A1 Атмосфера: {data.get('atmo')}\n"
        f"\U0001F4D0 Формат: {data.get('format')}\n\n"
        "Выбери, что хочешь изменить:"
    )

    keyboard = [
        [
            InlineKeyboardButton("\U0001F3A8 Стиль", callback_data="param:style"),
            InlineKeyboardButton("\U0001F3DE Сцена", callback_data="param:scene")
        ],
        [
            InlineKeyboardButton("\U0001F4A1 Атмосфера", callback_data="param:atmo"),
            InlineKeyboardButton("\U0001F4D0 Формат", callback_data="param:format")
        ],
        [InlineKeyboardButton("\U0001F3AF Сгенерировать", callback_data="generate_prompt_custom")]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    if hasattr(update_or_message, "edit_message_text"):
        await update_or_message.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)
    else:
        await update_or_message.reply_text(text, parse_mode="Markdown", reply_markup=markup)


async def prompt_param_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_prompt_menu(query, context)
