import os
import httpx
from dotenv import load_dotenv
from log import logger

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


async def ask_assistant(prompt: str, model: str = "mistralai/mistral-7b-instruct") -> str:
    print(model)
    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_URL, headers=HEADERS, json=body, timeout=30)
            if response.status_code != 200:
                logger.error(f"❌ Статус: {response.status_code}")
                logger.error(f"📩 Ответ: {response.text}")
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
            logger.info(f"🧠 Ответ от {model}: {reply}")
            return reply
    except Exception as e:
        logger.error(f"Ошибка генерации: {e}")
        raise
