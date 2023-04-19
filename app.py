from flask import Flask, render_template, g, current_app, request, jsonify
from helper import get_db, query_db, init_db
import sqlite3
import json


app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    plantid = request.args.get('plant-id')
    print("plant-id =",plantid, type(plantid))
    
    with open('data.txt', 'r') as f:
        data = f.read()
        print(data, type(data))
        records = json.loads(data)
        for record in records:
            print(records, type(records))
            print(record, type(record))
            print(record['plant-id'], type(record['plant-id']))
            if record['plant-id'] == int(plantid):
                return jsonify(record)
        return jsonify({'error': 'data not found'})

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
            return render_template("customer.html", customerFriendly=row["name"], customer=customer)
    
    return render_template("error.html", text="Customer not available")

@app.route("/<customer>/mapper")
def querytester(customer):
    init_db()
    
    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            return render_template("querytester.html", customerFriendly = row["name"], customer=customer) 
    
    return render_template("error.html", text="Customer for querytester not available")
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
