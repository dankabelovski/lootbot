import sqlite3
import os

DB_PATH = os.path.join("db", "lootbot.db")


def load_tools_from_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Получаем категории
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()  # [(1, "Автоматизация и интеграции"), ...]

    print("Категории из БД:", categories)

    tools_by_category = {}

    for cat_id, cat_name in categories:
        cursor.execute("""
            SELECT name, desc, url, post_link, scenarios
            FROM tools
            WHERE category_id = ?
        """, (cat_id,))
        tools = cursor.fetchall()

        tools_list = []
        for name, desc, url, post_link, scenarios_str in tools:
            scenarios = [s.strip() for s in scenarios_str.split(";")] if scenarios_str else []
            tool_id = name.lower().replace(" ", "")
            tools_list.append({
                "id": tool_id,
                "name": name,
                "desc": desc,
                "url": url,
                "post": post_link,
                "scenarios": scenarios
            })

        tools_by_category[cat_name] = tools_list

    conn.close()
    return tools_by_category


def get_tool_by_id(tool_id, category_name):
    tools_by_category = load_tools_from_sqlite()
    tools = tools_by_category.get(category_name, [])

    for tool in tools:
        if tool["id"] == tool_id:
            return tool

    return None


def load_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return {str(row[0]): row[1] for row in rows}  # {'1': 'Автоматизация и интеграции', ...}