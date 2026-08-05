class CategoryService:
    def __init__(self, storage) -> None:
        self.storage = storage.get_categories()
        self.id_to_name = {}
        self.name_to_id = {}

    def _build_id_lookup(self) -> None:
        for item in self.storage:
            self.id_to_name[f"{item[0]}"] = item[1]

    def _build_name_lookup(self) -> None:
        for item in self.storage:
            self.id_to_name[item[1]] = item[0]

    def get_category_name(self, category_id: int) -> str:
        return self.id_to_name[str(category_id)]

    def get_category_id(self, category_name: str) -> int:
        return self.name_to_id[category_name]
