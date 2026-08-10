from models.user import User
from storage.user_storage import UserStorage


class UserService:
    def __init__(self, user_storage: UserStorage):
        self.storage = user_storage

    def add_user(
        self,
        name: str,
        email: str,
        password_hash: str,
        contact: int,
    ) -> dict:
        name = name.strip()
        email = email.strip()
        password_hash = password_hash.strip()

        user = User(
            name,
            email,
            password_hash,
            contact,
        )

        added_user = self.storage.add_user(user)

        return {
            "user_id": added_user[0],
            "name": added_user[1],
            "email": added_user[2],
            "contact": added_user[3],
        }

    def get_user(self, user_id: int) -> dict:
        user = self.storage.get_user(user_id)

        return {
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
            "contact": user[3],
        }

    def update_user(self, user_id: int, updates: dict) -> dict:
        allowed_fields = {"name", "email", "contact"}

        if not updates:
            raise ValueError(f"Updates cannot be empty: {updates}.")

        for field, value in updates.items():
            if field not in allowed_fields:
                raise ValueError(f"Invalid update field: {field}")

        updated_user = self.storage.update_user(user_id, updates)

        return {
            "user_id": updated_user[0],
            "name": updated_user[1],
            "email": updated_user[2],
            "contact": updated_user[3],
        }

    def delete_user(self, user_id: int) -> bool:
        return self.storage.delete_user(user_id)
