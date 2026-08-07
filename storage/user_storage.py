from database.connection import get_connection
from models.user import User
from database.dynamic_query_builder import build_set_clause
from psycopg import sql


class UserStorage:
    def add_user(self, user: User) -> tuple:
        with get_connection() as connection:
            with connection.cursor() as cursor:
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

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"Failed to add the user: {user}. Please try again."
                    )

        return row

    def get_user(self, user_id: int) -> tuple:
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
                    raise ValueError(
                        f"User with id {user_id} not found.Please try again."
                    )

        return row

    def update_user(self, user_id: int, update_data: dict) -> tuple:
        set_clause, values = build_set_clause(update_data)
        values.append(user_id)

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("""
                        UPDATE users
                        SET {set_clause}
                        WHERE user_id = %s
                        RETURNING user_id, name, email, contact
                        """).format(set_clause=set_clause),
                    values,
                )

                row = cursor.fetchone()

                if row is None:
                    raise ValueError(
                        f"User with id {user_id} not found. Please try again."
                    )

        return row

    def delete_user(self, user_id: int) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE user_id = %s
                    RETURNING user_id
                    """,
                    (user_id,),
                )

                deleted = cursor.fetchone()

        return deleted is not None
