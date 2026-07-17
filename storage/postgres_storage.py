from database.connection import get_connection
from models.expense import Expense
from datetime import date


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

    def update_expense(
        self, expense_id: int, updates: dict[str, str | int | date]
    ) -> Expense:
        allowed_fields = {
            "category",
            "description",
            "amount",
            "expense_date",
        }

        if not updates:
            raise ValueError(f"Updates cannot be empty: {updates}")

        for field in updates:
            if field not in allowed_fields:
                raise ValueError(f"Invalid update field: {field}")

        set_clauses = []
        values = []

        for field, value in updates.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)

        set_clause = ", ".join(set_clauses)
        values.append(expense_id)

        query = f"""
            UPDATE expenses
            SET {set_clause}
            WHERE expense_id = %s
            RETURNING expense_id, category, description, amount, expense_date
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, values)

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError("Could not find expense.")

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
                    SELECT COALESCE(SUM(amount), 0)
                    FROM expenses
            """)

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError("Failed to retrieve total expenses.")

        return row[0]

    def get_spending_by_category(self, category: str) -> int:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT category, COALESCE(SUM(amount), 0)
                    FROM expenses
                    WHERE category = %s
                    GROUP BY category
                    """,
                    (category,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to fetch total expenses for the specified category: {category}"
                    )

        return row[1]

    def get_highest_spending_category(self) -> tuple[str | int] | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT category, COALESCE(SUM(amount), 0) AS total
                    FROM expenses
                    GROUP BY category
                    ORDER BY total DESC
                    LIMIT 1
                """)

                row = cursor.fetchone()

                if row is None:
                    return None

        return row

    def get_lowest_spending_category(self) -> tuple[str, int] | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT category, COALESCE(SUM(amount), 0) AS total
                    FROM expenses
                    GROUP BY category
                    ORDER BY total
                    LIMIT 1
                """)

                row = cursor.fetchone()

                if row is None:
                    return

        return row

    def get_category_spending(self) -> list[tuple]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT category, COALESCE(SUM(amount), 0) as total
                    FROM expenses
                    GROUP BY category
                    """)

                totals = cursor.fetchall()

        return totals
