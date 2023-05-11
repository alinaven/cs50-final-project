from flask import Flask, redirect, render_template, g, current_app, request, jsonify, url_for, flash
from helper import get_db, query_db, init_db
import sqlite3
import json


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'df2398459834fc6c2b9a5werd0208agk5d1c0fd37324febfgdd5506'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/<customer>', methods=['GET', 'POST'])
def api(customer):
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
            
        #check if input is empty
        #add error
        #if not plantformPriceColumn and plantformPriceTable:
            #flash('Both fields for price are required!')
        #elif not plantformNameColumn and plantformNameTable:
            #flash('Both fields for name are required!')
        #elif not plantformAmountColumn and plantformAmountTable:
            #flash('Both fields for amount are required!')
        #elif not plantformPictureColumn and plantformPictureTable:
            #flash('Both fields for picture are required!')
        #if all fields are filled
        #else:

    try: 
        open('data_' + customer + '.txt', 'r')
    except:
        return jsonify({'error': 'data source of this customer not found'})
    with open('data_' + customer + '.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        print("Records:", records, type(records))
        #loop through plants in endpoint data
        for record in records:
            if record['plant-id'] == plantid:
                print(plantid, type(plantid))
                # LOGIC TO SELECT RIGHT API OUTPUT AS VARIABLES
                print(plantformPriceTable)
                price = record[plantformPriceTable][plantformPriceColumn]
                name = record[plantformNameTable][plantformNameColumn]
                picture = record[plantformPictureTable][plantformPictureColumn]
                amount = record[plantformAmountTable][plantformAmountColumn]
                return render_template("mapper.html", plantid=plantid, price=price, name=name, picture=picture, amount=amount, customer=customer)
        return jsonify({'error': 'data not found'})

        
@app.route("/<customer>", methods=['GET', 'POST'])
def checkcustomer(customer):
    # Retrieve customer suffix's from database
    init_db()
    customerApi = '/api/' + customer
    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            return render_template("customer.html", customerFriendly=row["name"], customer=customer, customerApi=customerApi)
    
    return render_template("error.html", text="Customer not available")


#@app.route("/<customer>/mapper")
#def mapper(customer,plantid):
#    init_db()
#    
#    customers = query_db('select * from customers')
#    for row in customers:
#        if customer == row["suffix"]:
#            print(customer, plantid)
#            return render_template("mapper.html", customerFriendly = row["name"], customer=customer) 
#    
#    return render_template("error.html", text="Customer for querytester not available")
    

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
