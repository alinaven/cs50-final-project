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
        customerCap = customer.replace("_", " ")

        # Make first letter of each word uppercase
        customerFriendly = string.capwords(customerCap)

        return render_template("customer.html", customerFriendly=customerFriendly, customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")

@app.route("/<customer>/querytester")
def querytester(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        # Replace underscore with space
        customerCap = customer.replace("_", " ")

        # Make first letter of each word uppercase
        customerFriendly = string.capwords(customerCap)

        return render_template("querytester.html", customerFriendly=customerFriendly, customer=customer)
    else: 
        return render_template("error.html", text="Customer for querytester not available")
