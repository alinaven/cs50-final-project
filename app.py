from flask import Flask, render_template
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

<<<<<<< Updated upstream
@app.route("/<customer>")
def customerpage(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        # Replace underscore with space
        customer = customer.replace("_", " ")

        # Make first letter of each word uppercase
        customer = string.capwords(customer)

        return render_template("customer.html", customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")
=======
@app.route('/api/<customer>', methods=['GET', 'POST'])
def api(customer):
    # retrieve plantid from form on customer page
    plantid = request.form['plant-id']
    print("customer", customer, type(customer))
    
    print("plant-id =",plantid, type(plantid))
    try:
        open('data_'+customer+'.txt', 'r')
    except:
        return jsonify({'error': 'data source not found for this customer'})


    with open('data_'+customer+'.txt', 'r') as f:
        data = f.read()
        print(data, type(data))
        records = json.loads(data)
        #loop through plants in endpoint data
        for record in records:
            print(records, type(records),record, type(record), record['plant-id'], type(record['plant-id']))
            if record['plant-id'] == plantid:
                print(plantid, type(plantid))
                return jsonify(record)
        return jsonify({'error': 'data not found'})

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
>>>>>>> Stashed changes

@app.route("/<customer>/querytester")
def querytester(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        return render_template("querytester.html", customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")
