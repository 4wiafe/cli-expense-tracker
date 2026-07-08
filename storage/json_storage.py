import json
from models.expense import Expense


class JsonStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def _load(self) -> list[Expense]:
        try:
            with open(self.file_path, "r") as file:
                loaded_data = json.load(file)
                return [Expense.from_dict(data) for data in loaded_data]
        except FileNotFoundError:
            return []

    def _save(self, expenses: list[Expense]):
        with open(self.file_path, "w") as file:
            json.dump([expense.to_dict() for expense in expenses], file, indent=4)

    def add_expense(self, expense: Expense) -> Expense:
        expenses = self._load()
        expenses.append(expense)

        self._save(expenses)

        return expense

    def get_all_expenses(self) -> list[Expense]:
        return self._load()

    def find_by_id(self, expense_id: int) -> Expense | None:
        expenses = self._load()

        for expense in expenses:
            if expense.expense_id == expense_id:
                return expense

        return None

    def delete_expense(self, expense_id: int) -> bool:
        expenses = self._load()

        new_expenses = [
            expense for expense in expenses if expense.expense_id != expense_id
        ]
        self._save(new_expenses)

        return len(expenses) > len(new_expenses)
