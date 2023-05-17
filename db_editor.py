import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = lambda cursor, row: row[0]
print("Opened succesfully")

conn.execute('DROP TABLE customers')
conn.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, suffix TEXT NOT NULL, url TEXT NOT NULL)')
print("Table created succesfully")

conn.execute('INSERT INTO customers (name, suffix, url) VALUES (?, ?, ?)', ["Intratuin", "intratuin", '/api/intratuin-api'])
conn.execute('INSERT INTO customers (name, suffix, url) VALUES (?, ?, ?)', ["Het Oosten", "het_oosten", '/oosten-api'])

data = conn.execute('SELECT url FROM customers')
print(data)
print(data["url"])
conn.close()