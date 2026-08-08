from models.expense import Expense
from datetime import datetime
from services.category_service import CategoryService
from storage.expense_storage import ExpenseStorage


class ExpenseService:
    def __init__(
        self,
        storage: ExpenseStorage,
        category_service: CategoryService,
    ):
        self.storage = storage
        self.category_service = category_service

    def add_expense(
        self,
        user_id: int,
        category: str,
        description: str,
        amount: int,
        date: str,
    ) -> dict:
        expense_date = datetime.strptime(date, "%d-%m-%Y").date()

        category_name = category.strip().title()
        category_id = self.category_service.get_category_id(category_name)

        amount *= 100

        expense = Expense(
            category,
            description,
            amount,
            expense_date,
        )

        added_expense = self.storage.add_expense(user_id, category_id, expense)

        return {
            "expense_id": added_expense[0],
            "category": category_name,
            "description": added_expense[2],
            "amount": f"{added_expense[3] / 100:.2f}",
            "expense_date": added_expense[4].strftime("%d-%m-%Y"),
        }

    def list_all_expenses(self, user_id: int) -> list:
        expenses = []
        fetched_expenses = self.storage.get_all_expenses(user_id)

        for expense in fetched_expenses:
            expenses.append(
                {
                    "expense_id": expense[0],
                    "category": self.category_service.get_category_name(expense[1]),
                    "description": expense[2],
                    "amount": f"{expense[3] / 100:.2f}",
                    "expense_date": expense[4].strftime("%d-%m-%Y"),
                }
            )

        return expenses

    def find_expense_by_id(self, user_id: int, expense_id: int) -> dict:
        expense = self.storage.find_expense_by_id(user_id, expense_id)

        return {
            "expense_id": expense[0],
            "category": self.category_service.get_category_name(expense[1]),
            "description": expense[2],
            "amount": f"{expense[3] / 100:.2f}",
            "expense_date": expense[4].strftime("%d-%m-%Y"),
        }

    def update_expense(self, user_id: int, expense_id: int, updates: dict) -> dict:
        allowed_fields = {
            "category",
            "description",
            "amount",
            "expense_date",
        }

        update_data = {}

        if not updates:
            raise ValueError(f"Updates cannot be empty: {updates}")

        for field in updates:
            if field not in allowed_fields:
                raise ValueError(f"Invalid update field: {field}")

        for field, value in updates.items():
            if field == "category":
                update_data[field] = self.category_service.get_category_id(value)
            elif field == "expense_date":
                update_data[field] = datetime.strptime(value, "%d-%m-%Y").date()
            else:
                update_data[field] = value

        updated_expense = self.storage.update_expense(
            user_id,
            expense_id,
            update_data,
        )

        return {
            "expense_id": updated_expense[0],
            "category": self.category_service.get_category_name(updated_expense[1]),
            "description": updated_expense[2],
            "amount": f"{updated_expense[3] / 100:.2f}",
            "expense_date": updated_expense[4].strftime("%d-%m-%Y"),
        }

    def delete_expense(self, user_id: int, expense_id: int) -> bool:
        return self.storage.delete_expense(user_id, expense_id)
