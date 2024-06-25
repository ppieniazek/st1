import html

import requests


class QuizzAPI:
    def __init__(self):
        self.categories = requests.get("https://opentdb.com/api_category.php").json()[
            "trivia_categories"
        ]
        self.url = "https://opentdb.com/api.php?"

    def set_url(self, q_num, category=None, difficulty=None):
        self.url += f"amount={q_num}&type=multiple"
        if category:
            for item in self.categories:
                if item["name"] == category:
                    self.url += f"&category={item["id"]}"
                    break

        if difficulty:
            self.url += f"&difficulty={difficulty.lower()}"

    def set_questions(self):
        response = requests.get(self.url)
        questions = response.json()["results"]

        # Decoding html encoding
        for question in questions:
            question["question"] = html.unescape(question["question"])
            if "incorrect_answers" in question:
                question["incorrect_answers"] = [
                    html.unescape(answer) for answer in question["incorrect_answers"]
                ]
            if "correct_answer" in question:
                question["correct_answer"] = html.unescape(question["correct_answer"])

        self.questions = questions
