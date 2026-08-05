from database.connection import get_connection


class CategoryStorage:
    def get_categories(self) -> list[tuple]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT category_id, category_name
                    FROM categories
                    """)

                rows = cursor.fetchall()

        return rows
