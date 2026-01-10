def question_to_sql(question: str) -> str:
    q = question.lower()

    if "top" in q and "customer" in q:
        return """
        SELECT name, SUM(amount) AS total
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        GROUP BY name
        ORDER BY total DESC
        LIMIT 3
        """

    if "total spending" in q:
        return """
        SELECT SUM(amount) AS total_spending
        FROM orders
        """

    return "SELECT * FROM customers"
