from fastapi import FastAPI
from app.agent import question_to_sql
from app.db import run_read_query
from app.utils import is_safe_sql
import sqlite3
import os

app = FastAPI(title="Autonomous Data Analyst")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "ecomm.db")

@app.on_event("startup")
def startup_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
      id INTEGER PRIMARY KEY,
      name TEXT,
      city TEXT
    );

    CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY,
      customer_id INTEGER,
      amount REAL,
      FOREIGN KEY(customer_id) REFERENCES customers(id)
    );
    """)

    cur.execute("SELECT COUNT(*) FROM customers")
    if cur.fetchone()[0] == 0:
        cur.executescript("""
        INSERT INTO customers VALUES
        (1,'Ananya','Delhi'),
        (2,'Rahul','Mumbai'),
        (3,'Zoya','Hyderabad');

        INSERT INTO orders VALUES
        (1,1,500),
        (2,1,800),
        (3,2,900),
        (4,3,700),
        (5,3,300);
        """)

    conn.commit()
    conn.close()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/ask")
def ask(q: dict):
    question = q.get("question")
    sql = question_to_sql(question)

    if not is_safe_sql(sql):
        return {"error": "Unsafe SQL generated"}

    _, rows = run_read_query(sql)

    return {
        "question": question,
        "generated_sql": sql,
        "row_count": len(rows),
        "results": rows,
        "explanation": "This query calculates totals per customer and sorts them."
    }
