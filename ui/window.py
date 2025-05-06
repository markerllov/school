import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from core.logic import AppLogic


class MainWindow:
    def __init__(self, logic: AppLogic):
        self.logic = logic
        self.root = tk.Tk()
        self.root.title("Школьные задания с Mistral")
        self.root.geometry("900x650")

        self._setup_ui()
        self._update_ui()

    def _setup_ui(self):
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        grade_frame = tk.Frame(self.main_frame)
        grade_frame.pack(fill=tk.X, pady=10)

        tk.Label(grade_frame, text="Выберите класс:", font=("Arial", 12)).pack(side=tk.LEFT)

        self.grade_var = tk.IntVar(value=6)
        self.grade_combobox = ttk.Combobox(
            grade_frame,
            textvariable=self.grade_var,
            values=list(range(6, 12)),
            state="readonly",
            width=3,
            font=("Arial", 12)
        )
        self.grade_combobox.pack(side=tk.LEFT, padx=10)
        self.grade_combobox.bind("<<ComboboxSelected>>", self._on_grade_change)

        self.refresh_btn = tk.Button(
            grade_frame,
            text="Обновить вопросы",
            command=self._refresh_questions,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        )
        self.refresh_btn.pack(side=tk.RIGHT)

        self.question_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 12),
            wraplength=800,
            justify="left",
            bg="#f5f5f5",
            padx=10,
            pady=10
        )
        self.question_label.pack(fill=tk.X, pady=10)

        self.answer_entry = tk.Entry(
            self.main_frame,
            font=("Arial", 12),
            width=60
        )
        self.answer_entry.pack(pady=10, ipady=5)
        self.answer_entry.bind("<Return>", lambda _: self._on_answer())

        self.submit_button = tk.Button(
            self.main_frame,
            text="Ответить",
            command=self._on_answer,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            state=tk.DISABLED
        )
        self.submit_button.pack(pady=10, ipadx=20, ipady=5)

        self.progress_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=10)

        self.status_label = tk.Label(
            self.main_frame,
            text="Выберите класс и нажмите 'Обновить вопросы'",
            fg="gray"
        )
        self.status_label.pack()

    def _on_grade_change(self, event=None):
        self.logic.grade = self.grade_var.get()
        self._refresh_questions()

    def _refresh_questions(self):
        self.status_label.config(text="Генерация вопросов...", fg="blue")
        self.root.update()

        try:
            if self.logic.load_questions():
                self._update_ui()
                self.status_label.config(text="Вопросы готовы!", fg="green")
            else:
                self.status_label.config(text="Ошибка загрузки вопросов", fg="red")
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {str(e)}", fg="red")