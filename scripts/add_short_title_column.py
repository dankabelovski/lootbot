import sqlite3

conn = sqlite3.connect("db/lootbot.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE articles ADD COLUMN short_title TEXT")

conn.commit()
conn.close()

print("✅ Колонка short_title добавлена")
