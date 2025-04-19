import sqlite3

DB_PATH = "db/lootbot.db"

def find_articles_by_query(query: str) -> list:
    """
    Ищет статьи по заголовку или тегам.
    Возвращает список кортежей (id, short_title)
    """
    conn = sqlite3.connect("db/lootbot.db")
    cursor = conn.cursor()

    query_lower = query.lower()
    cursor.execute("SELECT id, short_title, tags FROM articles WHERE tags IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for article_id, short_title, tags in rows:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        if any(tag in query_lower for tag in tag_list):
            results.append((article_id, short_title))

    return results