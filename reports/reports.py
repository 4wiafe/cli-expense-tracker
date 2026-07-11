from datetime import datetime, date


class Reports:
    def __init__(self, storage):
        self.storage = storage

    def total_expenses(self) -> int:
        return self.storage.get_total_expenses()

    def total_by_category(self, category) -> dict:
        striped_category = category.strip()
        total = self.storage.get_total_by_category(striped_category)

        return {"category": striped_category, "total": total}

    def highest_expense_category(self) -> dict[str, int | str]:
        highest_expense = self.storage.get_highest_expense()

        return {
            "expense_id": highest_expense.expense_id,
            "category": highest_expense.category,
            "description": highest_expense.description,
            "amount": f"{highest_expense.amount / 100:.2f}",
            "expense_date": highest_expense.expense_date.strftime("%m-%d-%Y"),
        }

    def lowest_expense_cateory(self) -> dict[str, int | str | date]:
        lowest_expense = self.storage.get_lowest_expense()

        return {
            "expense_id": lowest_expense.expense_id,
            "category": lowest_expense.category,
            "description": lowest_expense.description,
            "amount": f"{lowest_expense.amount / 100:.2f}",
            "expense_date": lowest_expense.expense_date.strftime("%m-%d-%Y"),
        }
