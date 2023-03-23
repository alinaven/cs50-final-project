from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<customer>")
def customerpage(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        return render_template("customer.html", customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")

@app.route("/<customer>/querytester")
def querytester(customer):
    if (customer == "intratuin" or customer == "het_oosten"):
        return render_template("querytester.html", customer=customer)
    else: 
        return render_template("error.html", text="Customer not available")