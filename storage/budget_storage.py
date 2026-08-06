from models.budget import Budget
from database.connection import get_connection
from database.dynamic_query_builder import build_set_clause
from psycopg import sql
from psycopg import errors


class BudgetStorage:
    def add_budget(self, user_id: int, category_id: int, budget: Budget) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO budgets (user_id, category_id, amount, month, year)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING budget_id, category_id, amount, month, year;
                    """,
                    (
                        user_id,
                        category_id,
                        budget.amount,
                        budget.month,
                        budget.year,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to add the budget: {budget}. Please try again."
                    )

        return row

    def get_budget(self, user_id: int, budget_id: int) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT budget_id, 
                        category_id, 
                        amount, 
                        month, 
                        year
                    FROM budgets
                    WHERE user_id = %s AND budget_id = %s;
                    """,
                    (user_id, budget_id),
                )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Budget with id {budget_id} not found. Please try again."
                    )

        return row

    def update_budget(self, user_id: int, budget_id: int, update_data: dict) -> tuple:
        set_clause, values = build_set_clause(update_data)
        values.append(user_id)
        values.append(budget_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        sql.SQL("""
                            UPDATE budgets
                            SET {set_clause}
                            WHERE user_id = %s AND budget_id = %s
                            RETURNING budget_id, category_id, amount, month, year;
                            """).format(set_clause=set_clause),
                        values,
                    )
                except errors.UniqueViolation:
                    raise ValueError(
                        "A budget already exists for this category, month, and year."
                    )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Budget with id {budget_id} was not found. Please try again."
                    )

        return row

    def delete_budget(self, user_id: int, budget_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM budgets
                    WHERE user_id = %s AND budget_id = %s
                    RETURNING budget_id;
                    """,
                    (user_id, budget_id),
                )

                deleted = cursor.fetchone()

        return deleted is not None
