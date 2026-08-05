class CategoryService:
    def __init__(self, storage):
        self.storage = storage
        self.categories = self.storage.get_all_categories()

        self.id_to_name = {}
        self.name_to_id = {}

        self._build_id_lookup()
        self._build_name_lookup()

    def _build_id_lookup(self):
        for category_id, category_name in self.categories:
            self.id_to_name[category_id] = category_name

    def _build_name_lookup(self):
        for category_id, category_name in self.categories:
            self.name_to_id[category_name] = category_id

    def get_category_name(self, category_id: int) -> str:
        return self.id_to_name[category_id]

    def get_category_id(self, category_name: str) -> int:
        return self.name_to_id[category_name]
