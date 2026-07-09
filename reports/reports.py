class Reports:
    def __init__(self, storage):
        self.storage = storage

    def total_expenses(self) -> int:
        return self.storage.get_total_expenses()

    def total_by_category(self, category) -> dict:
        striped_category = category.strip()
        total = self.storage.get_total_by_category(striped_category)

        return {"category": striped_category, "total": total}

    def highest_expense_category(self):
        expenses = self.storage.load()
        categories_total = {}

        for expense in expenses:
            if expense.category not in categories_total:
                categories_total[expense.category] = expense.amount
            else:
                categories_total[expense.category] += expense.amount

        max_category = max(categories_total.items(), key=lambda item: item[1])[0]

        return {max_category: f"{categories_total[max_category] / 100:.2f}"}

    def lowest_expense_cateory(self):
        expenses = self.storage.load()
        categories_total = {}

        for expense in expenses:
            if expense.category not in categories_total:
                categories_total[expense.category] = expense.amount
            else:
                categories_total[expense.category] += expense.amount

        min_category = min(categories_total.items(), key=lambda item: item[1])[0]

        return {min_category: f"{categories_total[min_category] / 100:.2f}"}
