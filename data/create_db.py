import sqlite3

con = sqlite3.connect('data/ecomm.db')
cur = con.cursor()

cur.executescript(open('data/schema.sql').read())
cur.executescript(open('data/seed.sql').read())

con.commit()
con.close()

print('DB created successfully')
