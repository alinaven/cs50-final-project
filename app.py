from flask import Flask, render_template, g, current_app
from helper import make_friendly, get_db, query_db, init_db
import sqlite3



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<customer>")
def customerpage(customer):
    # Retrieve customer suffix's from database
    init_db()

    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            return render_template("customer.html", customerFriendly=make_friendly(customer), customer=customer)
    
    return render_template("error.html", text="Customer not available")

@app.route("/<customer>/querytester")
def querytester(customer):
    init_db()
    
    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            return render_template("querytester.html", customerFriendly=make_friendly(customer), customer=customer) 
    
    return render_template("error.html", text="Customer for querytester not available")
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()