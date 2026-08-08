from storage.salary_storage import SalaryStorage
from models.salary import Salary


class SalaryService:
    def __init__(self, storage: SalaryStorage):
        self.storage = storage

    def add_salary(
        self,
        user_id: int,
        amount: int,
        month: int,
        year: int,
    ) -> dict:
        amount *= 100

        salary = Salary(amount, month, year)
        added_salary = self.storage.add_salary(user_id, salary)

        return {
            "salary_id": added_salary[0],
            "amount": f"{added_salary[1] / 100:.2f}",
            "month": added_salary[2],
            "year": added_salary[3],
        }

    def get_salary(self, user_id: int, salary_id: int) -> dict:
        fetched_salary = self.storage.get_salary(user_id, salary_id)

        return {
            "salary_id": fetched_salary[0],
            "amount": f"{fetched_salary[1] / 100:.2f}",
            "month": fetched_salary[2],
            "year": fetched_salary[3],
        }

    def update_salary(self, user_id, salary_id: int, updates: dict) -> dict:
        allowed_fields = {"amount", "month", "year"}
        update_data = {}

        if not updates:
            raise ValueError(f"Updates cannot be empty: {updates}")

        for field, value in updates.items():
            if field not in allowed_fields:
                raise ValueError(f"Invalid update field: {field}")

            if field == "amount":
                update_data[field] = value * 100
            else:
                update_data[field] = value

        updated_salary = self.storage.update_salary(
            user_id,
            salary_id,
            update_data,
        )

        return {
            "salary_id": updated_salary[0],
            "amount": f"{updated_salary[1] / 100:.2f}",
            "month": updated_salary[2],
            "year": updated_salary[3],
        }

    def delete_salary(self, user_id: int, salary_id: int) -> bool:
        return self.storage.delete_salary(user_id, salary_id)
