# db/tags.py

import sqlite3

DB_PATH = "db/lootbot.db"

def get_all_tags() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM tools WHERE tags IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    tags = set()
    for row in rows:
        if row[0]:
            tags.update(tag.strip().lower() for tag in row[0].split(","))
    return list(tags)
