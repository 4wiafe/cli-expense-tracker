from database.connection import get_connection
from models.expense import Expense


class PostgresStorage:
    def add_expense(self, expense: Expense) -> Expense:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO expenses (category, description, amount, expense_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING expense_id, category, description, amount, expense_date
                    """,
                    (
                        expense.category,
                        expense.description,
                        expense.amount,
                        expense.expense_date,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError("Failed to add the expense.")

        return Expense(
            expense_id=row[0],
            category=row[1],
            description=row[2],
            amount=row[3],
            expense_date=row[4],
        )

    def get_all_expenses(self) -> list[Expense]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
            SELECT expense_id, category, description, amount, expense_date
            FROM expenses
            """)

                rows = cursor.fetchall()
                expenses = []

                for row in rows:
                    expense = Expense(
                        category=row[1],
                        description=row[2],
                        amount=row[3],
                        expense_date=row[4],
                        expense_id=row[0],
                    )

                    expenses.append(expense)

        return expenses

    def find_by_id(self, expense_id: int) -> Expense:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT expense_id, category, description, amount, expense_date
                    FROM expenses
                    WHERE expense_id = %s
                    """,
                    (expense_id,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(f"Expense with id {expense_id} not found.")

        return Expense(
            category=row[1],
            description=row[2],
            amount=row[3],
            expense_date=row[4],
            expense_id=row[0],
        )

    def delete_expense(self, expense_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM expenses
                    WHERE expense_id = %s
                    RETURNING expense_id
                    """,
                    (expense_id,),
                )

                row = cursor.fetchone()

        return row is not None

    def get_total_expenses(self) -> int:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT SUM(amount)
                    FROM expenses
            """)

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError("Failed to retrieve total expenses.")

        return row[0]

    def get_total_by_category(self, category: str) -> int:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT SUM(amount)
                    FROM expenses
                    WHERE category = %s
                    """,
                    (category,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        "Failed to fetch total expenses for the specified category."
                    )

        return row[0]

    def get_highest_expense(self) -> Expense | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT expense_id, category, description, amount, expense_date
                    FROM expenses
                    ORDER BY amount DESC
                    LIMIT 1
                """)

                row = cursor.fetchone()

                if row is None:
                    return None

        return Expense(
            expense_id=row[0],
            category=row[1],
            description=row[2],
            amount=row[3],
            expense_date=row[4],
        )

    def get_lowest_expense(self) -> Expense | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT expense_id, category, description, amount, expense_date
                    FROM expenses
                    ORDER BY amount
                    LIMIT 1
                """)

                row = cursor.fetchone()

                if row is None:
                    return

        return Expense(
            expense_id=row[0],
            category=row[1],
            description=row[2],
            amount=row[3],
            expense_date=row[4],
        )
