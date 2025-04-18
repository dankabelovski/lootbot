from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.cache import get_cached_tools, get_cached_categories
from utils.context_helpers import get_effective_message
from handlers.start import start_handler

# Показать список категорий
async def tools_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_effective_message(update)
    categories = get_cached_categories()

    keyboard = [
        [InlineKeyboardButton(f"\U0001F4E6 {name}", callback_data=f"tools:{cat_id}")]
        for cat_id, name in categories.items()
    ]
    # Добавим кнопку назад
    keyboard.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_main")])

    await message.reply_text(
        "Выбери категорию инструментов:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Показать инструменты выбранной категории
async def tools_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, category_id = query.data.split(":", maxsplit=1)
    categories = get_cached_categories()
    category_name = categories.get(category_id, "")
    tools_by_category = get_cached_tools()
    tools = tools_by_category.get(category_name)

    if not tools:
        await query.edit_message_text(
            text=f"\U0001F52E Платформа: *{category_name}*\n\n`Платформа не найдена`\n\n\U0001F615 Попробуй снова.",
            parse_mode="Markdown"
        )
        return

    keyboard = [
        [InlineKeyboardButton(tool["name"], callback_data=f"tool:{tool['id']}:{category_id}")]
        for tool in tools
    ]
    keyboard.append([InlineKeyboardButton("\u2B05 Назад к категориям", callback_data="go_tools")])

    await query.edit_message_text(
        text=f"\U0001F6E0 Инструменты из категории *{category_name}*:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Показать карточку инструмента
async def tool_detail_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, tool_id, category_id = query.data.split(":", maxsplit=2)
    except ValueError:
        await query.edit_message_text("\u26A0 Ошибка: неверный формат callback_data")
        return

    categories = get_cached_categories()
    category_name = categories.get(category_id, "")
    tools_by_category = get_cached_tools()
    tools = tools_by_category.get(category_name, [])
    tool = next((t for t in tools if t["id"] == tool_id), None)

    if not tool:
        await query.edit_message_text("\U0001F615 Инструмент не найден.")
        return

    text = f"\U0001F9F0 *{tool['name']}*\n\n{tool['desc']}\n"

    if tool["url"]:
        text += f"\n\U0001F517 [Сайт инструмента]({tool['url']})"
    if tool["post"]:
        text += f"\n\U0001F4EC [Пост в канале]({tool['post']})"

    keyboard = []

    if tool["scenarios"]:
        for i, sc in enumerate(tool["scenarios"], start=1):
            keyboard.append([InlineKeyboardButton(f"\U0001F4C1 Сценарий {i}", callback_data=f"scenarios:{tool_id}:{i}:{category_id}")])

    keyboard.append([InlineKeyboardButton("\u2B05 Назад к категории", callback_data=f"tools:{category_id}")])

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Показать выбранный сценарий инструмента
async def tool_scenarios_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, tool_id, scenario_index, category_id = query.data.split(":", maxsplit=3)
    categories = get_cached_categories()
    category_name = categories.get(category_id, "")
    tools_by_category = get_cached_tools()
    tools = tools_by_category.get(category_name, [])
    tool = next((t for t in tools if t["id"] == tool_id), None)

    if not tool or not tool["scenarios"]:
        await query.edit_message_text("\u26A0 Сценарий не найден.")
        return

    try:
        scenario_text = tool["scenarios"][int(scenario_index) - 1]
    except (IndexError, ValueError):
        await query.edit_message_text("\u26A0 Ошибка при загрузке сценария.")
        return

    keyboard = [
        [InlineKeyboardButton("\u2B05 Назад к инструменту", callback_data=f"tool:{tool_id}:{category_id}")]
    ]

    await query.edit_message_text(
        text=f"\U0001F4C1 *Сценарий использования:*\n\n{scenario_text}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Назад к списку категорий
async def tools_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await tools_handler(update, context)


# Назад к списку инструментов в категории
async def back_to_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category_id = query.data.split(":", maxsplit=1)
    await tools_callback(update, context)



async def back_to_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start_handler(update, context)
