from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Customer, Product, Order, Review, order_product
from forms import *
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_retail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

@app.route('/')
def landing_page():
    return 'product retail landing page'

@app.route('/signup')
def signup():
    return 'customer signup route'

@app.route('/login')
def login():
    customers = Customer.query.all()
    customer_dict = {'customers': [customer.to_dict() for customer in customers]}
    return customer_dict

@app.route('/customer/<int:id>/')
# @login_required
def customer(id):
    customers = Customer.query.all()
    return 'customer id route'


if __name__ == "__main__":
    app.run(debug=True)
