from storage.category_storage import CategoryStorage


class CategoryService:
    def __init__(self, storage: CategoryStorage):
        self.storage = storage
        self._categories = self.storage.get_categories()

        if not self._categories:
            raise RuntimeError("No categories found. Please seed the categories table.")

        self._id_to_name = {}
        self._name_to_id = {}

        self._build_id_lookup()
        self._build_name_lookup()

    def _build_id_lookup(self):
        for category_id, category_name in self._categories:
            self._id_to_name[category_id] = category_name

    def _build_name_lookup(self):
        for category_id, category_name in self._categories:
            self._name_to_id[category_name] = category_id

    def get_category_name(self, category_id: int) -> str:
        if category_id not in self._id_to_name:
            raise ValueError(f"Invalid category id: {category_id}. Please try again.")

        return self._id_to_name[category_id]

    def get_category_id(self, category_name: str) -> int:
        category_name = category_name.strip().title()

        if category_name not in self._name_to_id:
            raise ValueError(
                f"Invalid category name: {category_name}. Please try again."
            )

        return self._name_to_id[category_name]
