import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from core.logic import AppLogic


class MainWindow:
    def __init__(self, logic: AppLogic):
        self.logic = logic
        self.root = tk.Tk()
        self.root.title("Школьные задания")
        self.root.geometry("900x650")

        self._setup_ui()
        self._init_question_buttons()

    def _setup_ui(self):
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        tk.Label(control_frame, text="Класс:", font=("Arial", 12)).pack(side=tk.LEFT)

        self.grade_var = tk.IntVar(value=6)
        ttk.Combobox(
            control_frame,
            textvariable=self.grade_var,
            values=list(range(6, 12)),
            state="readonly",
            width=3,
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            control_frame,
            text="Обновить вопросы",
            command=self._refresh_questions
        ).pack(side=tk.LEFT)

        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=10)

        self.question_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 14),
            wraplength=900,
            justify="left",
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        self.question_label.pack(fill=tk.X, pady=10)

        self.answer_entry = tk.Entry(
            self.main_frame,
            font=("Arial", 14),
            width=70
        )
        self.answer_entry.pack(pady=10, ipady=5)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=15)

        ttk.Button(
            button_frame,
            text="Сохранить ответ",
            command=self._save_answer
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Проверить все ответы",
            command=self._check_all_answers
        ).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            self.main_frame,
            text="Выберите класс и обновите вопросы",
            fg="gray"
        )
        self.status_label.pack(pady=10)

    def _init_question_buttons(self):
        self.question_buttons = []
        for i in range(5):
            btn = ttk.Button(
                self.buttons_frame,
                text=f"Вопрос {i + 1}",
                command=lambda idx=i: self._select_question(idx)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.question_buttons.append(btn)

    def _refresh_questions(self):
        self.logic.grade = self.grade_var.get()
        self.status_label.config(text="Загрузка вопросов...", fg="blue")
        self.root.update()

        if self.logic.load_questions():
            self._update_question_buttons()
            self._select_question(0)
            self.status_label.config(text="Выберите вопрос для ответа", fg="black")
        else:
            self.status_label.config(text="Ошибка загрузки вопросов", fg="red")

    def _update_question_buttons(self):
        for i, btn in enumerate(self.question_buttons):
            state = "answered" if self.logic.user_answers[i] else "unanswered"
            btn.state(["!disabled"])
            btn.configure(style=f"{state}.TButton")

    def _select_question(self, question_idx):
        self.current_question_idx = question_idx
        question = self.logic.questions[question_idx]
        self.question_label.config(text=f"Вопрос {question_idx + 1}:\n{question}")

        self.answer_entry.delete(0, tk.END)
        if self.logic.user_answers[question_idx]:
            self.answer_entry.insert(0, self.logic.user_answers[question_idx])

        for i, btn in enumerate(self.question_buttons):
            if i == question_idx:
                btn.state(["pressed", "disabled"])
            else:
                btn.state(["!pressed", "!disabled"])

    def _save_answer(self):
        answer = self.answer_entry.get().strip()
        if answer:
            self.logic.user_answers[self.current_question_idx] = answer
            self._update_question_buttons()
            self.status_label.config(text=f"Ответ на вопрос {self.current_question_idx + 1} сохранён", fg="green")

    def _check_all_answers(self):
        correct = sum(1 for i in range(5)
                      if self.logic.user_answers[i]
                      and self.logic.user_answers[i].lower() == self.logic.answers[i].lower())

        if correct == 5:
            messagebox.showinfo("Поздравляем!", "Все ответы верные!")
            self.root.after(2000, self.root.destroy)
        else:
            messagebox.showinfo(
                "Результат",
                f"Правильных ответов: {correct} из 5\n"
                "Продолжайте работать над вопросами!"
            )

    def run(self):
        style = ttk.Style()
        style.configure("unanswered.TButton", foreground="black")
        style.configure("answered.TButton", foreground="green")
        style.map("answered.TButton", foreground=[("active", "green")])

        self.root.mainloop()