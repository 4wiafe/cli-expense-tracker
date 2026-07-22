from datetime import datetime, date


class Reports:
    def __init__(self, storage):
        self.storage = storage

    def total_expenses(self) -> int:
        return self.storage.get_total_expenses()

    def total_by_category(self, category) -> dict[str, int]:
        normalized_category = category.strip().capitalize()
        category_name, total = self.storage.get_spending_by_category(
            normalized_category
        )

        return {"category": category_name, "total": total}

    def highest_spending_category(self) -> dict[str, int | str]:
        highest_category = self.storage.get_highest_spending_category()

        return {highest_category[0]: f"{highest_category[1] / 100:.2f}"}

    def lowest_spending_cateory(self) -> dict[str, int | str]:
        lowest_category = self.storage.get_lowest_spending_category()

        return {lowest_category[0]: f"{lowest_category[1] / 100:.2f}"}

    def category_spending(self) -> list[dict]:
        all_spending_categories = []
        spending_categories = self.storage.get_category_spending()

        for spending_category in spending_categories:
            normalized_category = {
                spending_category[0]: f"{spending_category[1] / 100:.2f}"
            }

            all_spending_categories.append(normalized_category)

        return all_spending_categories
