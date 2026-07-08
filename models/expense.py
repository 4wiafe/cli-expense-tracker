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
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "expense_date": self.expense_date.strftime("%m-%d-%Y"),
            "expense_id": self.expense_id,
        }

    @staticmethod
    def from_dict(data) -> Expense:
        expense_date = datetime.strptime(data["expense_date"], "%m-%d-%Y").date()

        expense = Expense(
            data["category"],
            data["description"],
            data["amount"],
            expense_date,
            data["expense_id"],
        )

        return expense
