import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

MODELS = {
    "LootBot Generator": "https://dankabelov-lootbot-imagegen.hf.space"
}


def generate_image(prompt: str, space_url: str) -> bytes:
    import time
    import requests

    headers = {"Content-Type": "application/json"}
    payload = {"data": [prompt]}

    for attempt in range(5):
        try:
            res = requests.post(f"{space_url}/run/predict", headers=headers, json=payload)
            if res.status_code == 200:
                try:
                    output_url = res.json()["data"][0]
                    return requests.get(output_url).content
                except Exception as e:
                    raise Exception(f"Ошибка разбора JSON-ответа: {res.text}")
            else:
                print(f"Попытка {attempt+1}: статус {res.status_code}")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
        time.sleep(5)

    raise Exception(f"Невозможно получить изображение с {space_url}")

