from flask import Flask, render_template
from helper import make_friendly
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<customer>")
def customerpage(customer):
    # Retrieve customer suffix's from database
    conn = sqlite3.connect('database.db')
    conn.row_factory = lambda cursor, row: row[0]

    # TO DO: MIGRATE OUT THE CODE LINES WHERE WE ADD/INSERT DATA TO THE DATABASE WITHIN THESE PYTHON FUNCTION!
    conn.execute('DROP TABLE customers')
    conn.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, suffix TEXT NOT NULL)')
    conn.execute('INSERT INTO customers (name, suffix) VALUES (?, ?)', ["Intratuin", "intratuin"])
    conn.execute('INSERT INTO customers (name, suffix) VALUES (?, ?)', ["Het Oosten", "het_oosten"])
    cursor = conn.execute('SELECT suffix FROM customers')
    print(cursor)
    data = cursor.fetchall()
    print(data)
    if customer in data:
        return render_template("customer.html", customerFriendly=make_friendly(customer), customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")

@app.route("/<customer>/querytester")
def querytester(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        return render_template("querytester.html", customerFriendly=make_friendly(customer), customer=customer)
    else: 
        return render_template("error.html", text="Customer for querytester not available")