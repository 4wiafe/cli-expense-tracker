from psycopg import sql


def build_set_clause(update_data: dict) -> tuple:
    set_clauses = []
    values = []

    for field, value in update_data.items():
        set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(field)))
        values.append(value)

    set_clause = sql.SQL(", ").join(set_clauses)

    return set_clause, values
