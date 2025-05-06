import requests
import json
import logging
from typing import Tuple, List
from config import Config

logger = logging.getLogger(__name__)


class DeepSeekAPI:
    @staticmethod
    def generate_questions(grade: int) -> Tuple[List[str], List[str]]:
        try:
            prompt = f"""
            Сгенерируй 5 тестовых вопросов для {grade} класса по школьной программе.
            Включи вопросы из разных предметов: {', '.join(Config.SUBJECTS)}.
            Формат вывода (строго соблюдай):
            Вопрос: [текст вопроса]
            Ответ: [правильный ответ]
            ---
            """

            response = requests.post(
                Config.API_URL,
                headers={
                    "Authorization": f"Bearer {Config.MISTRAL_API_KEY}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json={
                    "model": Config.MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30
            )

            if response.status_code != 200:
                error_msg = f"Нет API {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return DeepSeekAPI._parse_response(content)

        except Exception as e:
            logger.error(f"Ошибка генерации вопосов: {str(e)}")
            raise

    @staticmethod
    def _parse_response(content: str) -> Tuple[List[str], List[str]]:
        questions = []
        answers = []

        blocks = content.split('---')
        for block in blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            question = None
            answer = None

            for line in lines:
                if line.startswith('Вопрос:'):
                    question = line[7:].strip()
                elif line.startswith('Ответ:'):
                    answer = line[6:].strip()

            if question and answer:
                questions.append(question)
                answers.append(answer)
                if len(questions) >= 5:
                    break

        return questions[:5], answers[:5]