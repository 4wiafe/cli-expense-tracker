from database.connection import get_connection
from models.expense import Expense


class PostgresStorage:
    def add_expense(self, expense: Expense) -> int:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (category, description, amount, expense_date)
            VALUES (%s, %s, %s, %s)
            RETURNING expense_id
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
            raise RuntimeError("Failed to retrieve generated expense ID.")

        expense_id = row[0]

        connection.commit()

        cursor.close()
        connection.close()

        return expense_id

    def get_all_expenses(self) -> list[Expense]:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT expense_id, category, description, amount, expense_date
            FROM expenses
            """)

        rows = cursor.fetchall()
        expense_objects = []

        for row in rows:
            expense = Expense(
                category=row[1],
                description=row[2],
                amount=row[3],
                expense_date=row[4],
                expense_id=row[0],
            )

            expense_objects.append(expense)

        cursor.close()
        connection.close()

        return expense_objects

    def find_by_id(self, expense_id: int) -> Expense:
        connection = get_connection()
        cursor = connection.cursor()

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
            raise RuntimeError("Failed to retrieve expense.")

        expense = Expense(
            category=row[1],
            description=row[2],
            amount=row[3],
            expense_date=row[4],
            expense_id=row[0],
        )

        cursor.close()
        connection.close()

        return expense

    def delete_expense(self, expense_id: int) -> bool:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM expenses
            WHERE expense_id = %s
            RETURNING expense_id
            """,
            (expense_id,),
        )

        deleted_expense = cursor.fetchone()

        connection.commit()

        success = deleted_expense is not None

        cursor.close()
        connection.close()

        return success
