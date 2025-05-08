from typing import Optional, Tuple, List
from api.mistral import MistralAPI


class AppLogic:
    def __init__(self, initial_grade: int = 6):
        self.grade = initial_grade
        self.questions: List[str] = []
        self.answers: List[str] = []
        self.user_answers: List[str] = []
        self.current_question = 0
        self.load_questions()

    def load_questions(self) -> bool:
        try:
            self.questions, self.answers = MistralAPI.generate_questions(self.grade)
            self.user_answers = [""] * len(self.questions)
            return len(self.questions) == 5
            return True
        except Exception as e:
            print(f"Ошибка загрузки вопросов: {e}")
            return False

    def next_grade(self):
        self.grade += 1
        if self.grade > 11:
            self.grade = 6
        return self.grade

    def check_answer(self, user_answer: str) -> bool:
        if self.current_question >= len(self.questions):
            return False

        self.user_answers[self.current_question] = user_answer
        is_correct = user_answer.lower() == self.answers[self.current_question].lower()
        self.current_question += 1
        return is_correct

    def get_current_question(self) -> Optional[str]:
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def get_question(self, index: int) -> Optional[Tuple[str, str]]:
        if 0 <= index < len(self.questions):
            return self.questions[index], self.answers[index]
        return None

    def get_progress(self) -> Tuple[int, int]:
        return self.current_question + 1, len(self.questions)

    def check_completion(self) -> bool:
        return all(
            user.lower() == correct.lower()
            for user, correct in zip(self.user_answers, self.answers)
        )