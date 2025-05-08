import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from core.logic import AppLogic


class MainWindow:
    def __init__(self, logic: AppLogic):
        self.logic = logic
        self.root = tk.Tk()
        self.root.title("Ад школьников")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f5f5f5")

        self._load_logo()
        self._setup_styles()
        self._create_widgets()
        self._init_state()

    def _load_logo(self):
        try:
            logo_path = os.path.join("assets", "logo.png")
            self.logo_img = Image.open(logo_path)
            self.logo_img = self.logo_img.resize((200, 80), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        except Exception as e:
            print(f"Не удалось загрузить логотип: {e}")
            self.logo_photo = None

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TLabel', background="#f5f5f5", font=('Helvetica', 11))
        style.configure('TButton', font=('Helvetica', 11))

        style.configure('Status.TLabel',
                        foreground="#666666",
                        font=('Helvetica', 10),
                        background="#f5f5f5")

        style.configure('Question.TButton',
                        foreground="#333333",
                        padding=10)

        style.map('Active.TButton',
                  foreground=[('active', 'white'), ('pressed', 'white')],
                  background=[('active', '#4285f4'), ('pressed', '#3367d6')])

        style.configure('Answered.TButton',
                        foreground="white",
                        background="#34a853")

        style.configure('Unanswered.TButton',
                        foreground="white",
                        background="#ea4335")

    def _create_widgets(self):
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=20, pady=10)

        if self.logo_photo:
            logo_label = ttk.Label(header, image=self.logo_photo)
            logo_label.pack(side=tk.LEFT)

        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(control_frame, text="Класс:").pack(side=tk.LEFT)

        self.grade_var = tk.IntVar(value=6)
        grade_combo = ttk.Combobox(
            control_frame,
            textvariable=self.grade_var,
            values=list(range(6, 12)),
            state="readonly",
            width=3
        )
        grade_combo.pack(side=tk.LEFT, padx=10)

        ttk.Button(
            control_frame,
            text="Обновить вопросы",
            command=self._refresh_questions
        ).pack(side=tk.LEFT)

        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.question_buttons = []
        for i in range(5):
            btn = ttk.Button(
                self.buttons_frame,
                text=f"Вопрос {i + 1}",
                style='Question.TButton',
                command=lambda idx=i: self._select_question(idx)
            )
            btn.pack(side=tk.LEFT, expand=True, padx=5)
            self.question_buttons.append(btn)

        self.question_text = tk.Text(
            self.root,
            wrap=tk.WORD,
            font=('Helvetica', 12),
            bg="#e3f2fd",
            padx=15,
            pady=15,
            height=6,
            relief="solid",
            borderwidth=1
        )
        self.question_text.pack(fill=tk.X, padx=20, pady=10)
        self.question_text.config(state=tk.DISABLED)

        self.answer_entry = ttk.Entry(
            self.root,
            font=('Helvetica', 12)
        )
        self.answer_entry.pack(pady=15, ipady=8, padx=20, fill=tk.X)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Сохранить ответ",
            command=self._save_answer
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Проверить все ответы",
            command=self._check_all_answers
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Скип",
            command=self._skipall
        ).pack(side=tk.LEFT, padx=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Выберите класс и обновите вопросы")
        self.status_label = ttk.Label(
            self.root,
            textvariable=self.status_var,
            style='Status.TLabel'
        )
        self.status_label.pack(pady=10)

    def _init_state(self):
        self.current_question_idx = 0
        self._update_question_buttons()
        self._select_question(0)

    def _refresh_questions(self):
        self.logic.grade = self.grade_var.get()
        self.status_var.set("Загрузка вопросов...")
        self.root.update()

        try:
            if self.logic.load_questions():
                self._update_question_buttons()
                self._select_question(0)
                self.status_var.set("Вопросы загружены. Выберите вопрос для ответа")
            else:
                self.status_var.set("Ошибка загрузки вопросов")
        except Exception as e:
            self.status_var.set(f"Ошибка: {str(e)}")

    def _update_question_buttons(self):
        for i, btn in enumerate(self.question_buttons):
            if i < len(self.logic.questions):
                btn.state(['!disabled'])
                if self.logic.user_answers[i]:
                    btn.configure(style='Answered.TButton')
                else:
                    btn.configure(style='Unanswered.TButton')
            else:
                btn.state(['disabled'])

    def _select_question(self, question_idx):
        self.current_question_idx = question_idx

        for i, btn in enumerate(self.question_buttons):
            if i == question_idx:
                btn.configure(style='Active.TButton')
            elif self.logic.user_answers[i]:
                btn.configure(style='Answered.TButton')
            else:
                btn.configure(style='Unanswered.TButton')

        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        if question_idx < len(self.logic.questions):
            self.question_text.insert(tk.END, self.logic.questions[question_idx])
        self.question_text.config(state=tk.DISABLED)

        self.answer_entry.delete(0, tk.END)
        if question_idx < len(self.logic.user_answers):
            self.answer_entry.insert(0, self.logic.user_answers[question_idx])

    def _save_answer(self):
        answer = self.answer_entry.get().strip()
        if answer and self.current_question_idx < len(self.logic.user_answers):
            self.logic.user_answers[self.current_question_idx] = answer
            self._update_question_buttons()
            self.status_var.set(f"Ответ на вопрос {self.current_question_idx + 1} сохранён")

    def _check_all_answers(self):
        if not hasattr(self.logic, 'answers') or not self.logic.answers:
            self.status_var.set("Сначала загрузите вопросы")
            return

        correct = 0
        total = min(len(self.logic.questions), len(self.logic.answers))

        for i in range(total):
            if (i < len(self.logic.user_answers)) and self.logic.user_answers[i]:
                if self.logic.user_answers[i].lower() == self.logic.answers[i].lower():
                    correct += 1

            if correct == total and total > 0:
                messagebox.showinfo("Поздравляем!", "Все ответы верные!")
            self.root.after(2000, self.root.destroy)
        else:
            messagebox.showinfo(
                "Результат",
                f"Правильных ответов: {correct} из {total}\n"
                "Продолжайте работать над вопросами!"
            )

    def _skipall(self):
        messagebox.showinfo("Поздравляем!", "Все ответы верные!")
        return

    def run(self):
        self.root.mainloop()