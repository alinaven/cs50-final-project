from flask import Flask, render_template, g, request, session, redirect, url_for
from flask_session import Session
from helper import get_db, query_db, init_db, login_required, apology, insertUser, retrieveUsers
import sqlite3
import json

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/<customerApi>', methods=['GET','POST'])
def api(customerApi):
    if request.method == "GET":
        return apology("No direct request is supported for this page")
    else:
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
        customers = query_db('select * from customers')
        for row in customers:
            if customerApi == row["urlconfig"]:
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
                conn.commit()
                try:
                    open(source, 'r')
                except:
                    return apology("Data source of this customer is not available")
                with open(source, 'r') as f:
                    data = f.read()
                    records = json.loads(data)
                    #loop through plants in endpoint data
                    for record in records:
                        if record['plant-id'] == plantid:
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
                        return apology("Plant-id not found")
        return apology("This API cannot be found")   

@app.route("/<customer>", methods=['GET'])
def checkcustomer(customer):
    #Retrieve customer suffix's from database
    customers = query_db('select * from customers')

    #Find match between customer parameter and database suffices
    for row in customers:
        if customer == row["suffix"]:
            return render_template("customer.html", customerFriendly=row["name"], customer=customer, customerApi=row["apiurl"], urlConfig=row["urlconfig"], pricetable=row["pricetable"], pricefield=row["pricefield"], nametable=row["nametable"], namefield=row["namefield"], amounttable=row["amounttable"], amountfield=row["amountfield"], picturetable=row["picturetable"], picturefield=row["picturefield"])
    return apology("Customer not available")

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "GET":
        # When GET request
        customers = query_db('select * from customers')
        urlConfigIntratuin = "" 
        urlConfigHetOosten = "" 
        for row in customers:
            if row["suffix"] == "intratuin":
                urlConfigIntratuin = row["urlconfig"]
            elif row["suffix"] == "het_oosten":
                urlConfigHetOosten = row["urlconfig"]
        return render_template("admin.html", urlConfigIntratuin=urlConfigIntratuin, urlConfigHetOosten=urlConfigHetOosten, username=session["username"])

    else:
        # When POST request
        urlConfigIntratuin = request.form['url-config-intratuin']
        urlConfigHetOosten = request.form['url-config-hetoosten']

        conn = sqlite3.connect('database.db')
        conn.execute("UPDATE customers SET urlconfig = ? WHERE suffix = ?", (urlConfigIntratuin, "intratuin"))
        conn.execute("UPDATE customers SET urlconfig = ? WHERE suffix = ?", (urlConfigHetOosten, "het_oosten"))
        conn.commit()
        customers = query_db('select * from customers')
        for row in customers:
            if row["urlconfig"] != row["apiurl"]:
                return apology("This Api endpoint is not available. Make sure to change configuration.")
      
        return render_template("admin.html", urlConfigIntratuin=urlConfigIntratuin, urlConfigHetOosten=urlConfigHetOosten, username=session["username"], message="API URL('s) succesfully saved!")


@app.route("/admin-login", methods=['GET','POST'])
def adminlogin():
    if request.method == "GET":
        return render_template("admin-login.html")
    if request.method == "POST":
        users = query_db('select * from users')
        for user in users:
            if user["username"] == request.form['admin-username'] and user["password"] == request.form['admin-password']:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect("/admin")
        else:
            return apology("No correct username + password combination")
        

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2:
            insertUser(username, password)
            users = retrieveUsers()
            return render_template('admin-register.html', users=users, message="Registration was successful")
        else: 
            return apology("Passwords didn't match")
   	    
    else:
   	    return render_template('admin-register.html')
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin-login")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()