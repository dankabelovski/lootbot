# services/tools_db.py

tools_by_category = {
    "Создание контента": [
        {
            "id": "midjourney",
            "name": "MidJourney",
            "desc": "Генерация иллюстраций по промптам",
            "url": "https://www.midjourney.com/"
        },
        {
            "id": "runwayml",
            "name": "RunwayML",
            "desc": "Создание видео и анимаций на базе текста",
            "url": "https://runwayml.com/"
        }
    ],
    "Автоматизация и интеграции": [
        {
            "id": "zapier",
            "name": "Zapier",
            "desc": "Интеграция Telegram с Google Sheets, Notion и др.",
            "url": "https://zapier.com/",
            "post": "https://t.me/loot_and_learn/91",  # пост о Zapier
            "scenarios": [
                "📤 Автопубликация новых заявок из Google Forms в Telegram",
                "📦 Отслеживание обновлений в Notion через бота"
            ]
        },
        {
            "id": "controllerbot",
            "name": "@ControllerBot",
            "desc": "Автопостинг и планирование контента",
            "url": "https://t.me/ControllerBot"
        }
    ],
    "Маркетинг и аналитика": [
        {
            "id": "tgstat",
            "name": "TGStat",
            "desc": "Аналитика каналов и постов",
            "url": "https://tgstat.ru/"
        }
    ],
    "Безопасность и приватность": [
        {
            "id": "protonvpn",
            "name": "ProtonVPN",
            "desc": "Надёжный VPN с фокусом на конфиденциальность",
            "url": "https://protonvpn.com/"
        }
    ],
    "Игровой и креативный AI": [
        {
            "id": "aidungeon",
            "name": "AI Dungeon",
            "desc": "Текстовые приключения с генерацией сюжета",
            "url": "https://play.aidungeon.io/"
        }
    ]
}
