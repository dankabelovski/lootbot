import sqlite3
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.context_helpers import get_effective_message
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "lootbot.db")
DB_PATH = os.path.abspath(DB_PATH)


async def insights_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_effective_message(update)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, COALESCE(short_title, title) FROM articles ORDER BY id DESC LIMIT 15")
    articles = cursor.fetchall()
    conn.close()

    if not articles:
        await message.reply_text("😕 Пока нет опубликованных статей.")
        return

    keyboard = [
        [InlineKeyboardButton(title, callback_data=f"article:{article_id}")]
        for article_id, title in articles
    ]
    keyboard.append([InlineKeyboardButton("🏠 Назад в меню", callback_data="back_to_main")])

    await message.reply_text(
        text="🧠 *Последние статьи:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def articles_by_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category_id = query.data.split(":")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM articles WHERE category_id = ?", (category_id,))
    articles = cursor.fetchall()
    conn.close()

    if not articles:
        await query.edit_message_text("😕 В этой категории пока нет статей.")
        return

    keyboard = [
        [InlineKeyboardButton(title, callback_data=f"article:{article_id}")]
        for article_id, title in articles
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="go_insights")])

    await query.edit_message_text(
        text="📄 Статьи в категории:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def article_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, article_id = query.data.split(":")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, post_link FROM articles WHERE id = ?", (article_id,))
    article = cursor.fetchone()
    conn.close()

    if not article:
        await query.edit_message_text("⚠️ Статья не найдена.")
        return

    title, desc, link = article
    text = f"*{title}*\n\n{desc}\n\n🔗 [Читать в канале]({link})"

    keyboard = [
        [InlineKeyboardButton("⬅️ Назад к статьям", callback_data="go_insights")],
        [InlineKeyboardButton("🏠 Назад в меню", callback_data="back_to_main")]
    ]
    await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


async def back_to_articles_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await insights_handler(update, context)