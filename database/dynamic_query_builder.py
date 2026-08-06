def build_set_clause(update_data: dict) -> tuple[str, list]:
    set_clauses = []
    values = []

    for field, value in update_data.items():
        set_clauses.append(f"{field} = %s")
        values.append(value)

    return ", ".join(set_clauses), values
