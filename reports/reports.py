class Reports:
    def __init__(self, storage):
        self.storage = storage

    def total_expenses(self):
        expenses = self.storage.load()
        total = 0

        for expense in expenses:
            total += expense.amount

        return total

    def total_by_category(self, category):
        striped_category = category.strip()
        expenses = self.storage.load()
        total = 0

        for expense in expenses:
            if striped_category == expense.category:
                total += expense.amount

        return f"{expense.category}: {total / 100:.2f}"

    def highest_expense_category(self):
        expenses = self.storage.load()
        amounts = []

        for expense in expenses:
            amounts.append(expense.amount)

        return f"{max(amounts) / 100:.2f}"

    def lowest_expense_cateory(self):
        expenses = self.storage.load()
        amounts = []

        for expense in expenses:
            amounts.append(expense.amount)

        return f"{min(amounts) / 100:.2f}"
