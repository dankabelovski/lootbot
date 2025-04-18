import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"

def ask_assistant(prompt: str) -> dict:
    instruction = (
        "Ты — ассистент Telegram-бота Loot & Learn. "
        "Ты помогаешь находить полезные инструменты из базы по описанию запроса пользователя. "
        "Отвечай как в обычном чате, не используй JSON, просто текст.\n"
        "Если нашёл подходящие инструменты — напиши это, но сами инструменты предложит бот позже."
    )

    full_prompt = f"{instruction}\n\nПользователь:\n{prompt}"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_predict": 200
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        raw = response.json().get("response", "")
        print("🧠 Ответ от Ollama:", raw)

        return {
            "reply": raw.strip(),
            "options": []
        }

    except Exception as e:
        print("⚠️ Ошибка phi3:", e)
        return {
            "reply": "⚠️ Не удалось получить ответ от ассистента.",
            "options": []
        }
