import json
from models.expense import Expense


class JsonStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return [Expense.from_dict(item) for item in data]
        except FileNotFoundError:
            return []

    def save(self, expenses):
        with open(self.file_path, "w") as file:
            json.dump([expense.to_dict for expense in expenses], file, indent=4)
