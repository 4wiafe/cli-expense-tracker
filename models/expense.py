from uuid import uuid4
from datetime import datetime, date


class Expense:
    def __init__(self, date: date, category: str, description: str, amount: int):
        self.id = str(uuid4())
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.created_at = str(datetime.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data) -> Expense:
        expense = Expense(
            data["date"], data["category"], data["description"], data["amount"]
        )
        expense.id = data["id"]

        return expense
