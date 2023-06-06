from flask import Flask, redirect, render_template, g, current_app, request, jsonify, url_for, flash
from helper import get_db, query_db, init_db
import sqlite3
import json


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/<customerApi>', methods=['GET', 'POST'])
def api(customerApi):
    # retrieve data from form on customer page
    plantid = request.form['plant-id']
    PriceTable = request.form['price-table']
    PriceField = request.form['price-field']
    NameTable = request.form['name-table']
    NameField = request.form['name-field']
    AmountTable = request.form['amount-table']
    AmountField = request.form['amount-field']
    PictureTable = request.form['picture-table']
    PictureField = request.form['picture-field']
            
    # Get data source for customer
    #init_db()
    customers = query_db('select * from customers')
    for row in customers:
        print('database entry: ' + row["url"])
        print('given by website: ' + customerApi)
        if customerApi == row["url"]:
            source = row["source"]
            customer = row["suffix"]
            conn = sqlite3.connect('database.db')
            conn.execute("UPDATE customers SET pricetable = ? WHERE suffix = ?", (PriceTable, customer))
            conn.execute("UPDATE customers SET pricefield = ? WHERE suffix = ?", (PriceField, customer))
            conn.execute("UPDATE customers SET nametable = ? WHERE suffix = ?", (NameTable, customer))
            conn.execute("UPDATE customers SET namefield = ? WHERE suffix = ?", (NameField, customer))
            conn.execute("UPDATE customers SET amounttable = ? WHERE suffix = ?", (AmountTable, customer))
            conn.execute("UPDATE customers SET amountfield = ? WHERE suffix = ?", (AmountField, customer))
            conn.execute("UPDATE customers SET picturetable = ? WHERE suffix = ?", (PictureTable, customer))
            conn.execute("UPDATE customers SET picturefield = ? WHERE suffix = ?", (PictureField, customer))
            result = conn.execute("SELECT picturetable FROM customers WHERE suffix = ?", (customer,)).fetchall()
            conn.commit()
            print("Result: ", result)
            print("Source: ", source)
            print(row["picturetable"])
            try:
                open(source, 'r')
            except:
                return jsonify({'error': 'data source of this customer not available'})
            with open(source, 'r') as f:
                data = f.read()
                records = json.loads(data)
                print("Records:", records, type(records))
                #loop through plants in endpoint data
                for record in records:
                    if record['plant-id'] == plantid:
                        # TO DO: hij stopt hier niet!
                        print(plantid, type(plantid))
                        # LOGIC TO SELECT RIGHT API OUTPUT AS VARIABLES
                        try: 
                            price = record[PriceTable][PriceField]
                        except: 
                            price = "Not available"
                        try:
                            name = record[NameTable][NameField]
                        except:
                            name = "Not available"
                        try: 
                            amount = record[AmountTable][AmountField]
                        except:
                            amount = "Not available"
                        try:
                            picture = record[PictureTable][PictureField]
                        except:
                            picture = "Not available"
                        return render_template("mapper.html", plantid=plantid, name=name, price=price, picture=picture, amount=amount, customer=customer, customerFriendly=row["name"])
                else:  
                    return jsonify({'error': 'Plant-id not found'})
    return jsonify({'error': 'no customer exist with this api'})

        
@app.route("/<customer>", methods=['GET', 'POST'])
def checkcustomer(customer):
    # Retrieve customer suffix's from database
    #init_db()
    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            print (customer)
            return render_template("customer.html", customerFriendly=row["name"], customer=customer, customerApi=row["url"], pricetable=row["pricetable"], pricefield=row["pricefield"], nametable=row["nametable"], namefield=row["namefield"], amounttable=row["amounttable"], amountfield=row["amountfield"], picturetable=row["picturetable"], picturefield=row["picturefield"])
    
    return render_template("error.html", text="Customer not available")   

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
