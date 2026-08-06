from database.connection import get_connection
from models.expense import Expense
from database.dynamic_query_builder import build_set_clause
from datetime import date
from psycopg import sql


class ExpenseStorage:
    def add_expense(
        self, user_id: int, category_id: int, expense: Expense
    ) -> tuple[str | int, ...]:
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
                        expense.category,
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
    ) -> tuple[str | int, ...]:
        set_clause, values = build_set_clause(update_data)
        values.append(user_id)
        values.append(expense_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("""
                        UPDATE expenses
                        SET {set_clause}
                        WHERE expense_id = %s AND user_id = %s
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

    def get_all_expenses(self, user_id: int) -> list[tuple]:
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

        return cursor.fetchall()

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
                    RETURNNING expense_id;
                    """,
                    (user_id, expense_id),
                )

        return cursor.fetchone() is not None
