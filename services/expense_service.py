from models.expense import Expense
from datetime import datetime


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def add_expense(
        self, category: str, description: str, amount: int, expense_date: str
    ) -> Expense:
        normalized_date = datetime.strptime(expense_date, "%d-%m-%Y").date()

        expense = Expense(category, description, amount, normalized_date)

        added_expense = self.storage.add_expense(expense)

        return added_expense

    def update_expense(self, expense_id, updates: dict[str, str | int]) -> Expense:
        normalized_expense_id = int(expense_id.strip())
        allowed_fields = {
            "category",
            "description",
            "amount",
            "expense_date",
        }

        normalized_updates = {}

        if not updates:
            raise ValueError(f"Updates cannot be empty: {updates}")

        for field, value in updates.items():
            if field not in allowed_fields:
                raise ValueError(f"Invalid update field: {field}")

            if field == "amount":
                if not isinstance(value, (int, str)):
                    raise ValueError(f"Invalid amount: {value}")

                value = int(value) * 100
            elif field == "expense_date":
                if not isinstance(value, (str)):
                    raise ValueError(f"Invalid date: {value}")

                value = datetime.strptime(value, "%d-%m-%Y").date()

            normalized_updates[field] = value

        updated_expense = self.storage.update_expense(
            normalized_expense_id, normalized_updates
        )

        return updated_expense

    def list_expenses(self) -> list[Expense]:
        return self.storage.get_all_expenses()

    def find_by_id(self, expense_id: int) -> Expense:
        return self.storage.find_by_id(expense_id)

    def delete_expense(self, expense_id: int) -> Expense:
        return self.storage.delete_expense(expense_id)
