from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import db, Customer, Product, Order, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_retail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

with app.app_context():
    db.create_all()

    customer = Customer(first_name="Sherwin",
                        last_name="Manchester",
                        username="sherman",
                        email= "smanchester@gmail.com",
                        address="222 Plum Ln Pocatello, Id",
                        hashed_password= "stheman")
    
    db.session.add(customer)
    db.session.commit()
    
    