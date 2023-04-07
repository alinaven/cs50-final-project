import string
from flask import g, current_app
import sqlite3

def make_friendly(customer):
    # Replace underscore with space
    # Make first letter of each word uppercase
    customerFriendly = string.capwords(customer.replace("_", " "))
    return customerFriendly

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))