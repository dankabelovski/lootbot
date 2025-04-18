# services/prompt_generator.py

def generate_prompt(platform: str) -> tuple[str, str]:
    prompts = {
        "MidJourney": (
            "/imagine prompt: futuristic samurai in neon rain, ultra-detailed, cinematic, 8k",
            "🎴 Используй для генерации постера или обложки в стиле киберпанк."
        ),
        "DALL·E": (
            "A surreal cityscape merging nature and technology, high detail, watercolor style",
            "🎨 Идеально для обложек статей или оформления Telegram-постов."
        ),
        "Stable Diffusion": (
            "A mystical forest with glowing mushrooms and fog, fantasy concept art",
            "🌲 Подойдёт для генерации фонов, ландшафтов, концепт-арта."
        )
    }

    return prompts.get(platform, ("Платформа не найдена", "😕 Попробуй снова."))
