from datetime import datetime, date


class Expense:
    def __init__(
        self,
        category: str,
        description: str,
        amount: int,
        expense_date: date,
        expense_id: int | None = None,
    ):
        self.category = category
        self.description = description
        self.amount = amount
        self.expense_date = expense_date
        self.expense_id = expense_id

    def to_dict(self) -> dict:
        return {
            "expense_id": self.expense_id,
            "category": self.category,
            "description": self.description,
            "amount": f"{self.amount / 100:.2f}",
            "expense_date": self.expense_date.strftime("%d-%m-%Y"),
        }

    @staticmethod
    def from_dict(expense_data: dict) -> Expense:
        expense_date = datetime.strptime(
            expense_data["expense_date"], "%d-%m-%Y"
        ).date()

        expense = Expense(
            expense_data["category"],
            expense_data["description"],
            expense_data["amount"],
            expense_date,
            expense_data["expense_id"],
        )

        return expense
