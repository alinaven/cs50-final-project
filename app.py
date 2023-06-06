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
    #TODO: werkt nog niet, want customerApi variabele in customer.html is nu zonder /api/.... waardoor hij de customer.html opnieuw laadt. Voeg api/.... toe aan customer.html form
    # retrieve data from form on customer page
    plantid = request.form['plant-id']
    plantformPriceTable = request.form['plantform-price-table']
    plantformPriceColumn = request.form['plantform-price-column']
    plantformNameTable = request.form['plantform-name-table']
    plantformNameColumn = request.form['plantform-name-column']
    plantformAmountTable = request.form['plantform-amount-table']
    plantformAmountColumn = request.form['plantform-amount-column']
    plantformPictureTable = request.form['plantform-picture-table']
    plantformPictureColumn = request.form['plantform-picture-column']
            
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
            conn.execute("UPDATE customers SET pricetable = ? WHERE suffix = ?", (plantformPriceTable, customer))
            conn.execute("UPDATE customers SET pricefield = ? WHERE suffix = ?", (plantformPriceColumn, customer))
            result = conn.execute("SELECT pricetable FROM customers WHERE suffix = ?", (customer,)).fetchall()
            conn.commit()
            print("Result: ", result)
            print("Source: ", source)
            print(row["pricetable"])
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
                            price = record[plantformPriceTable][plantformPriceColumn]
                        except: 
                            price = "Not available"
                        try:
                            name = record[plantformNameTable][plantformNameColumn]
                        except:
                            name = "Not available"
                        try:
                            picture = record[plantformPictureTable][plantformPictureColumn]
                        except:
                            picture = "Not available"
                        try: 
                            amount = record[plantformAmountTable][plantformAmountColumn]
                        except:
                            amount = "Not available"
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
            return render_template("customer.html", customerFriendly=row["name"], customer=customer, customerApi=row["url"], pricetable=row["pricetable"], pricefield=row["pricefield"])
    
    return render_template("error.html", text="Customer not available")   

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
