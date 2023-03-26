import sqlite3

conn = sqlite3.connect('database.db')
print("Opened succesfully")

#conn.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)')

intratuin = "Intratuin"
hetoosten = "Het Oosten"
conn.execute('INSERT INTO customers (name) VALUES (?)', [intratuin])
conn.execute('INSERT INTO customers (name) VALUES (?)', [hetoosten])

data = conn.execute('SELECT * FROM customers')
print(data.fetchall())