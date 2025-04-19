import os
import httpx

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://t.me/loot_and_learn_bot",
    "Content-Type": "application/json"
}

async def ask_assistant(prompt, model="mistral"):
    body = {
        "model": f"mistral/{model}",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_URL, headers=HEADERS, json=body, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Ошибка ассистента: {e}"