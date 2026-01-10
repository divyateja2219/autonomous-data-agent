def is_safe_sql(sql: str) -> bool:
    """
    Allow only SELECT queries for safety.
    Blocks DELETE, UPDATE, INSERT, DROP, etc.
    """
    sql = sql.strip().lower()
    return sql.startswith('select') or sql.startswith('with')
