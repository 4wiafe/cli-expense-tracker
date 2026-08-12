from database.connection import get_connection
from models.expense import Expense
from database.dynamic_query_builder import build_set_clause
from datetime import date
from psycopg import sql


class ExpenseStorage:
    # CRUD

    def add_expense(self, user_id: int, category_id: int, expense: Expense) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO expenses (user_id, category_id, description, amount, expense_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING expense_id, category_id, description, amount, expense_date;
                    """,
                    (
                        user_id,
                        category_id,
                        expense.description,
                        expense.amount,
                        expense.expense_date,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to add the expense: {expense}. Please try again."
                    )

        return row

    def update_expense(
        self, user_id, expense_id: int, update_data: dict[str, str | int | date]
    ) -> tuple:
        set_clause, values = build_set_clause(update_data)
        values.append(user_id)
        values.append(expense_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("""
                        UPDATE expenses
                        SET {set_clause}
                        WHERE user_id = %s AND expense_id = %s
                        RETURNING expense_id, category_id, description, amount, expense_date;
                        """).format(set_clause=set_clause),
                    values,
                )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Expense with id {expense_id} not found. Please try again."
                    )

        return row

    def get_all_expenses(self, user_id: int) -> list:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT expense_id, 
                        category_id, 
                        description, 
                        amount, 
                        expense_date
                    FROM expenses
                    WHERE user_id = %s;
                    """,
                    (user_id,),
                )

                rows = cursor.fetchall()

        return rows

    def find_expense_by_id(self, user_id: int, expense_id: int) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT expense_id, 
                        category_id, 
                        description, 
                        amount, 
                        expense_date
                    FROM expenses
                    WHERE user_id = %s AND expense_id = %s;
                    """,
                    (user_id, expense_id),
                )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Expense with id {expense_id} not found. Please try again."
                    )

        return row

    def delete_expense(self, user_id: int, expense_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM expenses
                    WHERE user_id = %s AND expense_id = %s
                    RETURNING expense_id;
                    """,
                    (user_id, expense_id),
                )

                deleted = cursor.fetchone()

        return deleted is not None

    # REPORTS
    def get_total_expenses(self, user_id: int) -> int:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0)
                    FROM expenses
                    WHERE user_id = %s;
                    """,
                    (user_id,),
                )

                row = cursor.fetchone()
                assert row is not None

        return row[0]

    def get_spending_by_category(self, user_id: int, category_id: int) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT %s AS category_id, COALESCE(SUM(amount), 0)
                    FROM expenses
                    WHERE user_id = %s AND category_id = %s;
                    """,
                    (category_id, user_id, category_id),
                )

                row = cursor.fetchone()
                assert row is not None

        return row

    def get_all_category_spending(self, user_id: int) -> list:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT category_id, COALESCE(SUM(amount), 0)
                    FROM expenses
                    WHERE user_id = %s
                    GROUP BY category_id;
                    """,
                    (user_id,),
                )

                rows = cursor.fetchall()

        return rows

    def get_highest_spending_category(self, user_id: int) -> list:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    WITH category_totals AS (
                        SELECT category_id, COALESCE(SUM(amount), 0) AS total
                        FROM expenses
                        WHERE user_id = %s
                        GROUP BY category_id
                    )
                    SELECT category_id, total
                    FROM category_totals
                    WHERE total = (
                        SELECT MAX(total)
                        FROM category_totals
                    );
                    """,
                    (user_id,),
                )

                rows = cursor.fetchall()

        return rows

    def get_lowest_spending_category(self, user_id: int) -> list:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    WITH category_totals AS (
                        SELECT category_id, COALESCE(SUM(amount), 0) AS total
                        FROM expenses
                        WHERE user_id = %s
                        GROUP BY category_id
                    )
                    SELECT category_id, total
                    FROM category_totals
                    WHERE total = (
                        SELECT MIN(total)
                        FROM category_totals
                    );
                    """,
                    (user_id,),
                )

                rows = cursor.fetchall()

        return rows
