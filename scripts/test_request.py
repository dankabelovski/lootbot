import requests

space_url = "https://dankabelov-lootbot-imagegen.hf.space"
prompt = "a futuristic city floating above the clouds"

response = requests.post(
    f"{space_url}/run/predict",
    headers={"Content-Type": "application/json"},
    json={"data": [prompt]}
)

print(f"Status: {response.status_code}")
print(response.text)
