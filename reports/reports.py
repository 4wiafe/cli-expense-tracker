from storage.expense_storage import ExpenseStorage
from storage.budget_storage import BudgetStorage
from services.category_service import CategoryService


class Reports:
    def __init__(
        self,
        expense_storage: ExpenseStorage,
        budget_storage: BudgetStorage,
        category_service: CategoryService,
    ):
        self.expense_storage = expense_storage
        self.budget_storage = budget_storage
        self.category_service = category_service

    def get_total_expenses(self, user_id: int) -> dict:
        total = self.expense_storage.get_total_expenses(user_id)

        return {"total spending": f"{total / 100:.2f}"}

    def get_spending_by_category(self, user_id: int, category_name: str) -> dict:
        category_id = self.category_service.get_category_id(category_name)

        fetched_category_id, total = self.expense_storage.get_spending_by_category(
            user_id, category_id
        )

        print(fetched_category_id, total)

        return {
            "category_name": self.category_service.get_category_name(
                fetched_category_id
            ),
            "total": f"{total / 100:.2f}",
        }

    def get_all_category_spending(self, user_id: int) -> list:
        all_spending_categories = []

        fetched_spendings = self.expense_storage.get_all_category_spending(user_id)

        for spending in fetched_spendings:
            spending_data = {
                "category_name": self.category_service.get_category_name(spending[0]),
                "total": f"{spending[1] / 100:.2f}",
            }

            all_spending_categories.append(spending_data)

        return all_spending_categories

    def get_highest_spending_category(self, user_id: int) -> list:
        highest_spendings = []

        spendings = self.expense_storage.get_highest_spending_category(user_id)

        for spending in spendings:
            spending_data = {
                "category_name": self.category_service.get_category_name(spending[0]),
                "total": f"{spending[1] / 100:.2f}",
            }

            highest_spendings.append(spending_data)

        return highest_spendings

    def get_lowest_spending_category(self, user_id: int) -> list:
        lowest_spendings = []

        spendings = self.expense_storage.get_lowest_spending_category(user_id)

        for spending in spendings:
            spending_data = {
                "category_name": self.category_service.get_category_name(spending[0]),
                "total": f"{spending[1] / 100:.2f}",
            }

            lowest_spendings.append(spending_data)

        return lowest_spendings

    def get_budget_spending(self, user_id: int) -> list:
        budget_spendings = []

        spendings = self.budget_storage.get_budget_spending(user_id)

        for spending in spendings:
            spending_data = {
                "category_id": spending[0],
                "budget": f"{spending[1] / 100:.2f}",
                "spending": f"{spending[2] / 100:.2f}",
                "remaining": f"{spending[3] / 100:.2f}",
                "flag": spending[4],
                "month": spending[5],
                "year": spending[6],
            }

            budget_spendings.append(spending_data)

        return budget_spendings
