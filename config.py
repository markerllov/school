import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    API_URL = "https://api.mistral.ai/v1/chat/completions"
    MODEL = "mistral-small"  # или "mistral-medium", "mistral-large"

    GRADES = list(range(6, 12))  # 6-11 классы
    SUBJECTS = [
        "Математика", "Русский язык", "История",
        "Физика", "Химия", "Биология", "География"
    ]