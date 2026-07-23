from database.connection import get_connection
from models.expense import Expense
from models.salary import Salary
from datetime import date
import psycopg


class PostgresStorage:
    def add_expense(self, expense: Expense, user_id: int) -> Expense:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT category_id
                    FROM categories
                    WHERE name = %s;
                    """,
                    (expense.category,),
                )

                category_id = cursor.fetchone()

                if category_id is None:
                    raise ValueError(f"Invalid category: {expense.category}")

                cursor.execute(
                    """
                    INSERT INTO expenses (user_id, category_id, description, amount, expense_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING expense_id, category_id, description, amount, expense_date;
                    """,
                    (
                        user_id,
                        category_id[0],
                        expense.description,
                        expense.amount,
                        expense.expense_date,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(f"Failed to add the expense: {expense}")

        return Expense(
            expense_id=row[0],
            category=expense.category,
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

        with get_connection() as connection:
            with connection.cursor() as cursor:
                for field, value in updates.items():
                    if field == "category":
                        cursor.execute(
                            """
                            SELECT category_id
                            FROM categories
                            WHERE name = %s;
                            """,
                            (value,),
                        )

                        row = cursor.fetchone()

                        if row is None:
                            raise RuntimeError(f"Failed to fetch category id: {value}")

                        set_clauses.append("category_id = %s")
                        values.append(row[0])
                        continue

                    set_clauses.append(f"{field} = %s")
                    values.append(value)

                set_clause = ", ".join(set_clauses)
                values.append(expense_id)

                cursor.execute(
                    f"""
                    UPDATE expenses as e
                    SET {set_clause}
                    FROM categories as c
                    WHERE e.expense_id = %s
                        AND e.category_id = c.category_id
                    RETURNING e.expense_id, c.name, e.description, e.amount, e.expense_date;
                    """,
                    values,
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(f"Could not find expense: {row}")

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
                    SELECT e.expense_id, c.name, e.description, e.amount, e.expense_date
                    FROM expenses AS e
                    JOIN categories AS c ON e.category_id = c.category_id;
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
                    SELECT e.expense_id, c.name, e.description, e.amount, e.expense_date
                    FROM expenses AS e
                    JOIN categories AS c ON e.category_id = c.category_id
                    WHERE e.expense_id = %s;
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

    def get_spending_by_category(self, category: str) -> tuple[str | int, ...]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT c.name, COALESCE(SUM(e.amount), 0) AS total
                    FROM categories AS c
                        LEFT JOIN expenses AS e ON e.category_id = c.category_id
                    WHERE c.name = %s
                    GROUP BY c.name;
                    """,
                    (category,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to fetch total expenses for the specified category: {category}"
                    )

        return row

    def get_highest_spending_category(self) -> list[tuple] | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT category_name, total
                    FROM (
                        SELECT c.name AS category_name,
                            COALESCE(SUM(e.amount), 0) AS total
                        FROM categories AS c
                            LEFT JOIN expenses AS e ON e.category_id = c.category_id
                        GROUP BY c.name
                        HAVING SUM(e.amount) > 0
                    ) AS category_totals
                    WHERE total = (
                        SELECT COALESCE(MAX(total), 0) AS highest_total
                        FROM (
                            SELECT c.name AS category_name,
                                COALESCE(SUM(e.amount), 0) AS total
                            FROM categories AS c
                                LEFT JOIN expenses AS e ON e.category_id = c.category_id
                            GROUP BY c.name
                            HAVING SUM(e.amount) > 0
                        ) AS category_totals
                    );
                """)

                row = cursor.fetchall()

                if row is None:
                    return None

        return row

    def get_lowest_spending_category(self) -> tuple[str, int] | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT category_name, total
                    FROM (
                        SELECT c.name AS category_name,
                            COALESCE(SUM(e.amount), 0) AS total
                        FROM categories AS c
                            LEFT JOIN expenses AS e ON e.category_id = c.category_id
                        GROUP BY c.name
                        HAVING SUM(e.amount) > 0
                    ) AS category_totals
                    WHERE total = (
                        SELECT COALESCE(MIN(total), 0) AS lowest_total
                        FROM (
                            SELECT c.name AS category_name,
                                COALESCE(SUM(e.amount), 0) AS total
                            FROM categories AS c
                                LEFT JOIN expenses AS e ON e.category_id = c.category_id
                            GROUP BY c.name
                            HAVING SUM(e.amount) > 0
                        ) AS category_totals
                    );
                """)

                row = cursor.fetchone()

                if row is None:
                    return

        return row

    def get_category_spending(self) -> list[tuple]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.name as category_name,
                    COALESCE(SUM(e.amount), 0) as total
                    FROM categories as c
                    LEFT JOIN expenses as e ON e.category_id = c.category_id
                    GROUP BY c.name;
                    """)

                totals = cursor.fetchall()

        return totals

    def add_salary(self, salary: Salary, user_id: int) -> tuple[int, ...]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        """
                        INSERT INTO salaries (user_id, amount, month, year)
                        VALUES (%s, %s, %s, %s)
                        RETURNING salary_id, amount, month, year;
                        """,
                        (
                            user_id,
                            salary.amount,
                            salary.month,
                            salary.year,
                        ),
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError(
                        f"You've already added a salary for {salary.month}/{salary.year}. Did you mean to update it instead?"
                    )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(f"Failed to add salary: {salary}")

                return row
