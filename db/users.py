import sqlite3

DB_PATH = "db/lootbot.db"

def init_users_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            llm_model TEXT DEFAULT 'mistralai/mistral-7b-instruct'
        );
    """)
    conn.commit()
    conn.close()


def upsert_user(telegram_id: int, username: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, username)
        VALUES (?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET username=excluded.username;
    """, (telegram_id, username))
    conn.commit()
    conn.close()


def get_user_model(telegram_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT llm_model FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'mistralai/mistral-7b-instruct'


def set_user_model(telegram_id: int, model_name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET llm_model = ? WHERE telegram_id = ?
    """, (model_name, telegram_id))
    conn.commit()
    conn.close()
