from database.connection import get_connection
from models.expense import Expense


class PostgresStorage:
    def add_expense(self, expense: Expense):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (category, description, amount, date)
            VALUES (%s, %s, %s, %s)
            """,
            (expense.category, expense.description, expense.amount, expense.date),
        )

        connection.commit()

        cursor.close()
        connection.close()
