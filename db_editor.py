import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = lambda cursor, row: row[0]
print("Opened succesfully")

conn.execute('DROP TABLE customers')
conn.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, suffix TEXT NOT NULL)')
conn.execute('INSERT INTO customers (name, suffix) VALUES (?, ?)', ["Intratuin", "intratuin"])
conn.execute('INSERT INTO customers (name, suffix) VALUES (?, ?)', ["Het Oosten", "het_oosten"])

cursor = conn.execute('SELECT suffix FROM customers')
data = cursor.fetchall()
test = "intratuin"
print(data)

if test in data:
    print("success!")

conn.close()