from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import question_to_sql
from app.db import run_read_query
from app.utils import is_safe_sql

app = FastAPI(title="Autonomous Data Analyst")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/ask")
def ask(q: Query):
    # 1. Convert question → SQL
    sql = question_to_sql(q.question)

    # 2. Safety check
    if not is_safe_sql(sql):
        raise HTTPException(status_code=400, detail="Unsafe SQL detected")

    # 3. Run query
    columns, rows = run_read_query(sql)

    # 4. Return structured response
    return {
        "question": q.question,
        "generated_sql": sql,
        "row_count": len(rows),
        "results": rows,
        "explanation": explain(sql)
    }

def explain(sql: str) -> str:
    if "SUM" in sql and "GROUP BY" in sql:
        return "This query calculates totals per customer and sorts them."
    if "JOIN" in sql:
        return "This query combines customers with their orders."
    return "This query retrieves data from the database."
