import os
import httpx
from dotenv import load_dotenv
from log import logger

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
REFERER = os.getenv("OPENROUTER_REFERER")  # теперь опциональный

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Добавляем HTTP-Referer только если он есть в .env
if REFERER:
    HEADERS["HTTP-Referer"] = REFERER


async def ask_assistant(messages: list, model: str = "mistralai/mistral-7b-instruct") -> str:
    body = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_URL, headers=HEADERS, json=body, timeout=30)
            response.raise_for_status()
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            logger.info(f"🧠 Ответ от {model}: {reply}")
            return reply
    except Exception as e:
        logger.error(f"Ошибка генерации: {e}")
        raise