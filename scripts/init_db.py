import sqlite3
import os

DB_PATH = os.path.join("db", "lootbot.db")

os.makedirs("db", exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    desc TEXT,
    url TEXT,
    post_link TEXT,
    scenarios TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
""")

conn.commit()
conn.close()
print("✅ База lootbot.db создана со всеми таблицами.")
