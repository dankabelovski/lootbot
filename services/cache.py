from services.tools_loader import load_tools_from_sqlite, load_categories

tools_cache = None
categories_cache = None

def get_cached_tools():
    global tools_cache
    if tools_cache is None:
        tools_cache = load_tools_from_sqlite()
    return tools_cache

def get_cached_categories():
    global categories_cache
    if categories_cache is None:
        categories_cache = load_categories()
    return categories_cache

def reload_cache():
    global tools_cache, categories_cache
    tools_cache = load_tools_from_sqlite()
    categories_cache = load_categories()
    return True
