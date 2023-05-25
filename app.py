from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Customer, Product, Order, Review

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
    return 'customer login route'

@app.route('/customer/<int:id>/')
# @login_required
def customer(id):
    customers = Customer.query.all()
    return 'customer id route'


with app.app_context():
    db.create_all()

    # customer = Customer(first_name="Sherwin",
    #                     last_name="Manchester",
    #                     username="sherman",
    #                     email= "smanchester@gmail.com",
    #                     address="222 Plum Ln Pocatello, Id",
    #                     hashed_password= "stheman")

    product = Product(product_name="Oversized Chicago Bulls 6 Rings T-Shirt",
                        product_desc="Images from the Chicago Bulls final championship during their dynamic run of winning 6 NBA championships in the 90s.",
                        in_stock=10,
                        product_price= 24.99,
                        product_category="Shirts",
                        )

    # db.session.add(customer)
    db.session.add(product)
    db.session.commit()
