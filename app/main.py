from fastapi import FastAPI
from app.agent import question_to_sql
from app.db import run_read_query
from app.utils import is_safe_sql
import data.create_db

app = FastAPI(title="Autonomous Data Analyst")

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
