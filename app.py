from flask import Flask, render_template
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/<customer>/querytester")
def querytester(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        return render_template("querytester.html", customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")