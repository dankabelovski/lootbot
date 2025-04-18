import sqlite3

conn = sqlite3.connect("db/lootbot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    post_link TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
""")

conn.commit()
conn.close()

print("✅ Таблица articles с category_id создана")
