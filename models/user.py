class User:
    def __init__(
        self,
        name: str,
        email: str,
        password_hash: str,
        contact: int,
        user_id: int | None = None,
    ):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.contact = contact
        self.user_id = user_id
