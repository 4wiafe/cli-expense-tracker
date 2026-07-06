from models.expense import Expense


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def add_expense(self, date, category, description, amount):
        expense = Expense(date, category, description, amount)
        self.storage.add_expense(expense)

        return expense

    def list_expenses(self):
        return self.storage.get_all_expenses()

    def find_by_id(self, expense_id):
        return self.storage.find_by_id(expense_id)

    def delete_expense(self, expense_id):
        return self.storage.delete_expense(expense_id)
