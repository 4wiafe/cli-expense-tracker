from database.connection import get_connection
from models.expense import Expense
from models.salary import Salary
from models.budget import Budget
from models.user import User
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
        allowed_fields = {"category", "description", "amount", "expense_date"}

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
                    RETURNING expense_id;
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

    def update_salary(self, salary_id: int, updates: dict[str, int]) -> Salary:
        allowed_fields = {"amount", "month", "year"}

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
        values.append(salary_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        f"""
                        UPDATE salaries
                        SET {set_clause}
                        WHERE salary_id = %s
                        RETURNING salary_id, amount, month, year;
                        """,
                        values,
                    )

                except psycopg.errors.UniqueViolation:
                    raise ValueError(
                        "The salary you tried to upadte has duplicate data. Please try again"
                    )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to update the salary with id: {salary_id}"
                    )

            return Salary(
                amount=row[1],
                month=row[2],
                year=row[3],
                salary_id=row[0],
            )

    def get_salary(self, salary_id: int) -> Salary:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT salary_id, amount, month, year
                    FROM salaries
                    WHERE salary_id = %s;
                    """,
                    (salary_id,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to fetch the salary with id: {salary_id}"
                    )

                return Salary(
                    amount=row[1],
                    month=row[2],
                    year=row[3],
                    salary_id=row[0],
                )

    def delete_salary(self, salary_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM salaries
                    WHERE salary_id = %s
                    RETURNING salary_id;
                    """,
                    (salary_id,),
                )

                row = cursor.fetchone()

                return row is not None

    def add_budget(self, user_id: int, budget: Budget) -> Budget:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT category_id
                    FROM categories
                    WHERE name  = %s;
                    """,
                    (budget.category,),
                )

                category_id = cursor.fetchone()

                if category_id is None:
                    raise RuntimeError(
                        f"Failed to fetch category id of: {budget.category}"
                    )

                try:
                    cursor.execute(
                        """
                        INSERT INTO budgets (user_id, category_id, amount, month, year)
                        VALUES(%s, %s, %s, %s, %s)
                        RETURNING budget_id, category_id, amount, month, year;
                        """,
                        (
                            user_id,
                            category_id[0],
                            budget.amount,
                            budget.month,
                            budget.year,
                        ),
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError(
                        f"You've already added a budget for {budget.category} in {budget.month}/{budget.year}. Did you mean to update it instead?"
                    )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"Failed to add budget: {budget}. Please try again"
                    )

                return Budget(
                    category=budget.category,
                    amount=row[2],
                    month=row[3],
                    year=row[4],
                    budget_id=row[0],
                )

    def update_budget(self, budget_id: int, updates: dict[str, int]) -> Budget:
        allowed_fields = {"category", "amount", "month", "year"}

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

                        category_id = cursor.fetchone()

                        if category_id is None:
                            raise ValueError(f"Failed to fetch category id for {field}")

                        set_clauses.append(f"category_id = %s")
                        values.append(category_id[0])
                        continue

                    set_clauses.append(f"{field} = %s")
                    values.append(value)

                set_clause = ", ".join(set_clauses)
                values.append(budget_id)

                try:
                    cursor.execute(
                        f"""
                        UPDATE budgets as b
                        SET {set_clause}
                        FROM categories as c
                        WHERE b.budget_id = %s
                            AND c.category_id = b.category_id
                        RETURNING b.budget_id, c.name, b.amount, b.month, b.year;
                        """,
                        values,
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError(
                        "The budget you tried to update has duplicate data. Please try again"
                    )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError("Failed to update budget. Please try again")

                return Budget(
                    budget_id=row[0],
                    category=row[1],
                    amount=row[2],
                    month=row[3],
                    year=row[4],
                )

    def get_budget(self, budget_id: int) -> Budget:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT b.budget_id, c.name, b.amount, b.month, b.year
                    FROM budgets as b
                    JOIN categories as c ON c.category_id = b.category_id
                    WHERE b.budget_id = %s;
                    """,
                    (budget_id,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError("Failed to fetch budget. Please try again")

                return Budget(
                    budget_id=row[0],
                    category=row[1],
                    amount=row[2],
                    month=row[3],
                    year=row[4],
                )

    def delete_budget(self, budget_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM budgets
                    WHERE budget_id = %s
                    RETURNING budget_id;
                    """,
                    (budget_id,),
                )

                row = cursor.fetchone()

                return row is not None

    def get_budget_spending(self, user_id: int) -> list[tuple]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT c.name AS category,
                        b.amount AS budget,
                        COALESCE(SUM(e.amount), 0) AS spending,
                        (b.amount - COALESCE(SUM(e.amount), 0)) AS difference,
                        CASE
                            WHEN b.amount >= COALESCE(SUM(e.amount), 0) THEN 'Within Budget'
                            ELSE 'Over Budget'
                        END AS flag,
                        b.month,
                        b.year
                    FROM budgets AS b
                        LEFT JOIN expenses as e ON e.user_id = b.user_id
                        AND e.category_id = b.category_id
                        AND EXTRACT(MONTH FROM e.expense_date) = b.month
                        AND EXTRACT(YEAR FROM e.expense_date) = b.year
                        LEFT JOIN categories AS c ON c.category_id = b.category_id
                    WHERE b.user_id = %s
                    GROUP BY c.name, b.amount, b.month, b.year;
                    """,
                    (user_id,),
                )

                rows = cursor.fetchall()

                return rows

    def add_user(self, user: User) -> tuple[str | int, ...]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        """
                        INSERT INTO users (name, email, password_hash, contact)
                        VALUES(%s, %s, %s, %s)
                        RETURNING user_id, name, email, contact;
                        """,
                        (
                            user.name,
                            user.email,
                            user.password_hash,
                            user.contact,
                        ),
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError(
                        f"User with email {user.email} already exists. Please try again with a different email."
                    )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError("Failed to add user. Please try again.")

                return row

    def get_user(self, user_id: int) -> tuple[str | int, ...]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id, name, email, contact
                    FROM users
                    WHERE user_id = %s;
                    """,
                    (user_id,),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to fetch user with id {user_id}. Please try again."
                    )

                return row

    def update_user(
        self, user_id: int, updates: dict[str, str | int]
    ) -> tuple[str | int, ...]:
        allowed_fields = {"name", "email", "contact"}

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
        values.append(user_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        f"""
                        UPDATE users
                        SET {set_clause}
                        WHERE user_id = %s
                        RETURNING user_id, name, email, contact;
                        """,
                        values,
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError(
                        "That email is already in use by another account. Please try a different one."
                    )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        "Failed to update user details. Please try again."
                    )

                return row

    def delete_user(self, user_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE user_id = %s
                    RETURNING user_id;
                    """,
                    (user_id,),
                )

                row = cursor.fetchone()

                return row is not None
