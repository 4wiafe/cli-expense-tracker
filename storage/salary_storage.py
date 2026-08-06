from models.salary import Salary
from database.connection import get_connection
from psycopg import sql
from psycopg import errors
from database.dynamic_query_builder import build_set_clause


class SalaryStorage:
    def add_salary(self, user_id: int, salary: Salary) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO salaries (user_id, amount, month, year)
                    VALUES (%s, %s, %s, %s)
                    RETURNING salary_id, amount, month, year
                    """,
                    (
                        user_id,
                        salary.amount,
                        salary.month,
                        salary.year,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to add the salary: {salary}. Please try again."
                    )

        return row

    def get_salary(self, user_id: int, salary_id: int) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT salary_id,
                        amount,
                        month,
                        year
                    FROM salaries
                    WHERE user_id = %s AND salary_id = %s;
                    """,
                    (user_id, salary_id),
                )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Salary with id {salary_id} not found. Please try again."
                    )

        return row

    def update_salary(self, user_id, salary_id: int, update_data: dict) -> tuple:
        set_clause, values = build_set_clause(update_data)
        values.append(user_id)
        values.append(salary_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        sql.SQL("""
                        UPDATE salaries
                        SET {set_clause}
                        WHERE user_id = %s AND salary_id = %s
                        RETURNING salary_id, amount, month, year;
                        """).format(set_clause=set_clause),
                        values,
                    )

                except errors.UniqueViolation:
                    raise ValueError(
                        "The salary you tried to update has duplicate data. Please try again."
                    )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Salary with id {salary_id} was not found. Please try again."
                    )

        return row

    def delete_salary(self, user_id: int, salary_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM salaries
                    WHERE user_id = %s AND salary_id = %s
                    RETURNING salary_id;
                    """,
                    (user_id, salary_id),
                )

                deleted = cursor.fetchone()

        return deleted is not None
