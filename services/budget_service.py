from models.budget import Budget
from storage.budget_storage import BudgetStorage
from services.category_service import CategoryService


class BudgetService:
    def __init__(
        self,
        storage: BudgetStorage,
        category_service: CategoryService,
    ):
        self.storage = storage
        self.category_service = category_service

    def add_budget(
        self,
        user_id: int,
        category: str,
        amount: int,
        month: int,
        year: int,
    ) -> dict:
        category_id = self.category_service.get_category_id(category)
        amount *= 100

        budget = Budget(category, amount, month, year)

        added_budget = self.storage.add_budget(
            user_id,
            category_id,
            budget,
        )

        return {
            "budget_id": added_budget[0],
            "category": self.category_service.get_category_name(added_budget[1]),
            "amount": f"{added_budget[2] / 100:.2f}",
            "month": added_budget[3],
            "year": added_budget[4],
        }

    def get_budget(self, user_id: int, budget_id: int) -> dict:
        budget = self.storage.get_budget(user_id, budget_id)

        return {
            "budget_id": budget[0],
            "category": self.category_service.get_category_name(budget[1]),
            "amount": f"{budget[2] / 100:.2f}",
            "month": budget[3],
            "year": budget[4],
        }

    def update_budget(self, user_id: int, budget_id: int, updates: dict) -> dict:
        allowed_fields = {"category", "amount", "month", "year"}
        update_data = {}

        if not updates:
            raise ValueError(f"Updates cannot be empty: {updates}.")

        for field, value in updates.items():
            if field not in allowed_fields:
                raise ValueError(f"Invalid update field: {field}.")

            if field == "category":
                update_data[field] = self.category_service.get_category_id(value)
            elif field == "amount":
                update_data[field] = value * 100
            else:
                update_data[field] = value

        updated_budget = self.storage.update_budget(user_id, budget_id, update_data)

        return {
            "budget_id": updated_budget[0],
            "category": self.category_service.get_category_name(updated_budget[1]),
            "amount": f"{updated_budget[2] / 100:.2f}",
            "month": updated_budget[3],
            "year": updated_budget[4],
        }

    def delete_budget(self, user_id: int, budget_id: int) -> bool:
        return self.storage.delete_budget(user_id, budget_id)
