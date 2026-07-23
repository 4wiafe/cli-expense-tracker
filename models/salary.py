class Salary:
    def __init__(
        self,
        amount: int,
        month: int,
        year: int,
        salary_id: int | None = None,
    ):
        self.amount = amount
        self.month = month
        self.year = year
        self.salary_id = salary_id
