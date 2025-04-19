# services/db.py
import sqlite3

def set_user_model(user_id: int, model_id: str):
    conn = sqlite3.connect("db/lootbot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET llm_model = ? WHERE telegram_id = ?", (model_id, user_id))
    conn.commit()
    conn.close()

def get_user_model(user_id: int) -> str:
    conn = sqlite3.connect("db/lootbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT llm_model FROM users WHERE telegram_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "mistralai/mistral-7b-instruct"
