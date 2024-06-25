import random
from tkinter import StringVar

import customtkinter as ctk

from quizz_api import QuizzAPI


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.api = QuizzAPI()

        self.score = 0
        self.title("Quizz Game")
        self.geometry("600x400")
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()

    def setup_ui(self):
        # Number of Questions
        self.clear_widgets()
        self.number_label = ctk.CTkLabel(
            self, text="Number of Questions:", font=("Arial", 12)
        )
        self.number_label.pack(pady=(20, 5))
        self.number_var = StringVar(value="10")
        self.number_entry = ctk.CTkEntry(
            self,
            width=200,
            placeholder_text="10",
            font=("Arial", 12),
            textvariable=self.number_var,
        )
        self.number_entry.pack(pady=(0, 20))

        # Select Category
        self.category_label = ctk.CTkLabel(
            self, text="Select Category:", font=("Arial", 12)
        )
        self.category_label.pack(pady=(5, 5))
        self.category_var = StringVar(value="Any")
        self.category_menu = ctk.CTkOptionMenu(
            self,
            variable=self.category_var,
            values=["Any"] + [category["name"] for category in self.api.categories],
            font=("Arial", 12),
        )
        self.category_menu.pack(pady=(0, 20))

        # Select Difficulty
        self.difficulty_label = ctk.CTkLabel(
            self, text="Select Difficulty:", font=("Arial", 12)
        )
        self.difficulty_label.pack(pady=(5, 5))
        self.difficulty_var = StringVar(value="Any")
        self.difficulty_menu = ctk.CTkOptionMenu(
            self,
            variable=self.difficulty_var,
            values=["Any", "Easy", "Medium", "Hard"],
            font=("Arial", 12),
        )
        self.difficulty_menu.pack(pady=(0, 20))

        # Generate API URL Button
        self.generate_button = ctk.CTkButton(
            self,
            text="Generate API URL",
            command=self.generate_api_url,
            font=("Arial Bold", 12),
            fg_color=("light blue", "blue"),  # Subtle color change for the button
        )
        self.generate_button.pack(pady=(20, 10))

    def generate_api_url(self):
        try:
            q_num = int(self.number_entry.get())
        except ValueError:
            self.number_var.set("Enter a valid number!")
            return
        category = None if self.category_var.get() == "Any" else self.category_var.get()
        difficulty = (
            None if self.difficulty_var.get() == "Any" else self.difficulty_var.get()
        )

        self.api.set_url(q_num, category, difficulty)
        self.api.set_questions()

        self.clear_widgets()
        self.display_questions()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def display_questions(self):
        self.question_label = ctk.CTkLabel(
            self, text="", font=("Arial", 14), wraplength=500
        )
        self.question_label.pack(pady=(20, 25))

        self.answer1_var = StringVar(value="")
        self.answer1 = ctk.CTkButton(
            self,
            textvariable=self.answer1_var,
            command=lambda: self.next_question(self.answer1_var.get()),
            font=("Arial", 12),
            fg_color=("light gray", "gray"),
        )
        self.answer1.pack(pady=(0, 20))

        self.answer2_var = StringVar(value="")
        self.answer2 = ctk.CTkButton(
            self,
            textvariable=self.answer2_var,
            command=lambda: self.next_question(self.answer2_var.get()),
            font=("Arial", 12),
            fg_color=("light gray", "gray"),
        )
        self.answer2.pack(pady=(0, 20))

        self.answer3_var = StringVar(value="")
        self.answer3 = ctk.CTkButton(
            self,
            textvariable=self.answer3_var,
            command=lambda: self.next_question(self.answer3_var.get()),
            font=("Arial", 12),
            fg_color=("light gray", "gray"),
        )
        self.answer3.pack(pady=(0, 20))

        self.answer4_var = StringVar(value="")
        self.answer4 = ctk.CTkButton(
            self,
            textvariable=self.answer4_var,
            command=lambda: self.next_question(self.answer4_var.get()),
            font=("Arial", 12),
            fg_color=("light gray", "gray"),
        )
        self.answer4.pack(pady=(0, 20))

        self.current = 0
        self.display_question()

    def next_question(self, answer):
        if answer == self.api.questions[self.current]["correct_answer"]:
            self.score += 1
        self.current += 1
        if self.current < len(self.api.questions):
            self.display_question()
        else:
            self.display_score()

    def display_score(self):
        self.clear_widgets()
        self.score_label = ctk.CTkLabel(
            self,
            text=f"Score: {self.score/len(self.api.questions)*100:.2f}% ({self.score}/{len(self.api.questions)})",
            font=("Arial Bold", 14),
        )
        self.score_label.pack(pady=(20, 10))

        self.back_to_setup_button = ctk.CTkButton(
            self,
            text="Back to Setup",
            command=self.setup_ui,
            font=("Arial Bold", 12),
        )
        self.back_to_setup_button.pack(pady=(10, 0))

        self.restart_button = ctk.CTkButton(
            self,
            text="Restart",
            command=self.generate_api_url,
            font=("Arial Bold", 12),
        )
        self.restart_button.pack(pady=(10, 10))

        self.quit_button = ctk.CTkButton(
            self, text="Quit", command=self.quit, font=("Arial Bold", 12)
        )
        self.quit_button.pack(pady=(0, 20))

    def display_question(self):
        self.question_label.configure(text=self.api.questions[self.current]["question"])
        answers = self.api.questions[self.current]["incorrect_answers"][:]
        answers.append(self.api.questions[self.current]["correct_answer"])

        random.shuffle(answers)
        for answer, button_var in zip(
            answers,
            [
                self.answer1_var,
                self.answer2_var,
                self.answer3_var,
                self.answer4_var,
            ],
        ):
            button_var.set(answer)


app = App()
app.mainloop()
