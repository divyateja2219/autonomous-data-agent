import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "ecomm.db")

os.makedirs(DATA_DIR, exist_ok=True)

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
print("Database ready")
