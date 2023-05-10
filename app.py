from flask import Flask, redirect, render_template, g, current_app, request, jsonify, url_for, flash
from helper import get_db, query_db, init_db
import sqlite3
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df2398459834fc6c2b9a5werd0208agk5d1c0fd37324febfgdd5506'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/<customer>', methods=['GET', 'POST'])
def api(customer):
    # retrieve plantid from form on customer page
    plantid = request.form['plant-id']
    
    try: 
        open('data_' + customer + '.txt', 'r')
    except:
        return jsonify({'error': 'data source of this customer not found'})
    with open('data_' + customer + '.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        #loop through plants in endpoint data
        for record in records:
            if record['plant-id'] == plantid:
                print(plantid, type(plantid))
                record = jsonify(record)
        #return jsonify({'error': 'data not found'})
        #check if input is empty
        #add error
        if request.method == 'POST':
            plantformPrice = request.form['plantform-price-table']+request.form['plantform-price-column']
            plantformName = request.form['plantform-name-table']+request.form['plantform-name-column']
            plantformAmount = request.form['plantform-amount-table']+request.form['plantform-amount-column']
            plantformPicture = request.form['plantform-picture-table']+request.form['plantform-picture-column']
        if not plantformPrice:
            flash('Field for price is required!')
        elif not plantformName:
            flash('Field for name is required!')
        elif not plantformAmount:
            flash('Field for Amount is required!')
        elif not plantformPicture:
            flash('Field for Picture is required!')
        #if all fields are filled
        else:
            return redirect("/mapper.html")

        return render_template("customer.html")

@app.route("/<customer>", methods=['GET'])
def checkcustomer(customer):
    # Retrieve customer suffix's from database
    init_db()
    customerApi = '/api/' + customer
    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            return render_template("customer.html", customerFriendly=row["name"], customer=customer, customerApi=customerApi)
    
    return render_template("error.html", text="Customer not available")


@app.route("/<customer>/mapper")
def mapper(customer):
    init_db()
    
    customers = query_db('select * from customers')
    for row in customers:
        if customer == row["suffix"]:
            return render_template("mapper.html", customerFriendly = row["name"], customer=customer) 
    
    return render_template("error.html", text="Customer for querytester not available")
    

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
