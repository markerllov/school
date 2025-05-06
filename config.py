import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    API_URL = "https://api.mistral.ai/v1/chat/completions"
    MODEL = "mistral-small"

    GRADES = list(range(6, 12))
    SUBJECTS = [
        "Математика", "Русский язык", "История",
        "Физика", "Химия", "Биология", "География"
    ]