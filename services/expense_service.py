from models.expense import Expense
from datetime import datetime


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def add_expense(
        self, category: str, description: str, amount: int, expense_date: str
    ) -> Expense:
        normalized_date = datetime.strptime(expense_date, "%m-%d-%Y").date()

        expense = Expense(category, description, amount, normalized_date)

        self.storage.add_expense(expense)

        return expense

    def list_expenses(self) -> list[Expense]:
        return self.storage.get_all_expenses()

    def find_by_id(self, expense_id: int) -> Expense:
        return self.storage.find_by_id(expense_id)

    def delete_expense(self, expense_id: int) -> Expense:
        return self.storage.delete_expense(expense_id)
