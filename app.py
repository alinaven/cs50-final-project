from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/intratuin")
def intratuin():
    customer = "Intratuin"
    return render_template("customer.html", customer=customer)

@app.route("/hetoosten")
def hetoosten():
    customer = "Het Oosten"
    return render_template("customer.html", customer=customer)