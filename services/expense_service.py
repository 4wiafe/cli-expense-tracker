from models.expense import Expense


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage
        self.expenses = self.storage.load()

    def add_expense(self, date, category, description, amount):
        expense = Expense(date, category, description, amount)
        self.expenses.append(expense)
        self.storage.save(self.expenses)

        return expense

    def list_expenses(self):
        return self.expenses

    def find_by_id(self, expense_id):
        for exp in self.expenses:
            if exp.id == expense_id:
                return exp

        return None

    def delete_expense(self, expense_id):
        self.expenses = [exp for exp in self.expenses if exp.id != expense_id]
        self.storage.save(self.expenses)

        return self.expenses
