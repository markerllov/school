import requests
import json
from config import Config


class DeepSeekAPI:
    @staticmethod
    def generate_questions(grade: int) -> tuple[list[str], list[str]]:
        headers = {
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""Сгенерируй 5 тестовых вопросов для {grade} класса по школьной программе. 
        Включи вопросы из разных предметов: {', '.join(Config.SUBJECTS)}.
        Формат вывода (обязательно строго соблюдай):
        Вопрос: [текст вопроса]
        Ответ: [правильный ответ]
        ---
        Вопрос: [текст вопроса]
        Ответ: [правильный ответ]"""

        data = {
            "model": Config.MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        try:
            response = requests.post(
                Config.API_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return DeepSeekAPI._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса к API: {str(e)}")
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {str(e)}")

    @staticmethod
    def _parse_response(response: dict) -> tuple[list[str], list[str]]:
        content = response["choices"][0]["message"]["content"]
        questions = []
        answers = []

        blocks = content.split('---')
        for block in blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            question = None
            answer = None

            for line in lines:
                if line.startswith('Вопрос:'):
                    question = line.replace('Вопрос:', '').strip()
                elif line.startswith('Ответ:'):
                    answer = line.replace('Ответ:', '').strip()

            if question and answer:
                questions.append(question)
                answers.append(answer)

        return questions[:5], answers[:5]