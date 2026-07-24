class Budget:
    def __init__(
        self,
        category: str,
        amount: int,
        month: int,
        year: int,
        budget_id: int | None = None,
    ):
        self.category = category
        self.amount = amount
        self.month = month
        self.year = year
        self.budget_id = budget_id
