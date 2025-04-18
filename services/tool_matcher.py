import sqlite3

def find_tools_by_query(query: str) -> list:
    """
    Ищет инструменты по ключевым словам в поле tags.
    Возвращает список кортежей: (id, name)
    """
    conn = sqlite3.connect("db/lootbot.db")
    cursor = conn.cursor()

    query_lower = query.lower()

    cursor.execute("SELECT id, name, tags FROM tools WHERE tags IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for tool_id, name, tags in rows:
        if not tags:
            continue
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        if any(tag in query_lower for tag in tag_list):
            results.append((tool_id, name))

    return results
