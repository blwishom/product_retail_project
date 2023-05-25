from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import db, Customer, Product, Order, Review, order_product
import datetime

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
    
    product =   Product(product_name = "T-Shirt",
                        product_desc = "A classic through and through, Gap mens long sleeve t shirts the ideal addition to his wardrobe. With a soft jersey knit, long sleeves, a crew neckline, and banded cuffs, Gap long sleeve shirts for men are a must for his lifestyle.",
                        in_stock = 12,
                        product_price = 14.99,
                        product_category = "CLOTHING",
                        product_brand = "GAP")

    #how can we get our order price to be calculated based on product and quantity
    order =     Order(price = 31.57, 
                      date = datetime.datetime.today(),
                      customer_id = 1,
                      product_id = 1)
    
    review =    Review(customer_id = 1,
                       product_id = 1,
                       rating = 4.5,
                       comment = '''This is a wonderful product and the material is great. 
                       Definitely Will be buying more products like this.''',
                       created_at = datetime.datetime.today())

    order_product_data = [
            {'order_id': 1, 'product_id': 1, 'quantity': 2}
        ]
    
    for data in order_product_data:
        db.session.execute(order_product.insert().values(data))

    db.session.add(customer)
    db.session.add(product)
    db.session.add(order)
    db.session.add(review)
    db.session.commit()
    
    