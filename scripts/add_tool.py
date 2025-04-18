import sqlite3
import os

DB_PATH = os.path.join("db", "lootbot.db")

def list_categories(cursor):
    cursor.execute("SELECT id, name FROM categories")
    return cursor.fetchall()

def add_category(cursor, name):
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    return cursor.lastrowid

def add_tool(cursor, name, desc, url, post_link, scenarios, category_id):
    cursor.execute("""
        INSERT INTO tools (name, desc, url, post_link, scenarios, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, desc, url, post_link, scenarios, category_id))

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("📦 Существующие категории:")
    categories = list_categories(cursor)

    if categories:
        for cat in categories:
            print(f"{cat[0]} — {cat[1]}")
    else:
        print("⚠️ Нет категорий. Сначала добавим одну.")

    choice = input("\nВыбери ID категории или введи 'new' для новой: ")

    if choice.lower() == "new":
        new_cat_name = input("Название новой категории: ").strip()
        category_id = add_category(cursor, new_cat_name)
        print(f"✅ Добавлена категория с ID {category_id}")
    else:
        category_id = int(choice)

    name = input("Название инструмента: ").strip()
    desc = input("Описание: ").strip()
    url = input("Ссылка: ").strip()
    post_link = input("Ссылка на пост (можно оставить пустым): ").strip()
    scenarios = input("Сценарии (через ;): ").strip()

    add_tool(cursor, name, desc, url, post_link or None, scenarios, category_id)
    conn.commit()
    conn.close()

    print(f"\n✅ Инструмент '{name}' добавлен в категорию ID {category_id}")

if __name__ == "__main__":
    main()
