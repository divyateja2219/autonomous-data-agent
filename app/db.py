import sqlite3
from pathlib import Path

DB_PATH = Path("data/ecomm.db")

def run_read_query(sql: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    columns = rows[0].keys() if rows else []

    result = [dict(row) for row in rows]

    conn.close()
    return columns, result
