from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<pass>@localhost:3306/<DB>'
db = SQLAlchemy(app)


###Models####
class Review(db.Model):
    __tablename__ = "review"
    review_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    rating = db.Column(db.Float)
    comment = db.Column(db.String(255))
    created_at = db.Column(db.Datetime)
    price = db.Column(db.Integer)
    customer = db.relationship("Customer", backref="customer")
    product = db.relationship("Product", backref="product")

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self, review_id, customer_id, product_id,  rating, comment, created_at, price):
        self.rating = rating
        self.review_id = review_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.price = price
    def __repr__(self):
        return '' % self.id
db.create_all()