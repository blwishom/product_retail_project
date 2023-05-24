from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<pass>@localhost:3306/<DB>'
db = SQLAlchemy(app)


###Models####
# CUSTOMER MODEL
class Customer(db.Model, UserMixin):
    __tablename__ = "customer"

    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, email, username, address):
        self.email = email
        self.username = username
        self.address = address

    def __repr__(self):
        return '' % self.id

# PRODUCT MODEL
class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_desc = db.Column(db.String(255))
    in_stock = db.Column(db.Integer, nullable=False )
    product_price = db.Column(db.Integer, nullable=False )
    product_category = db.Column(db.String(255))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,produt_name,product_desc,in_stock,product_price,product_category):
        self.produt_name = produt_name
        self.product_desc = product_desc
        self.in_stock = in_stock
        self.product_price = product_price
        self.product_category = product_category
    def __repr__(self):
        return '' % self.id

# REVIEW MODEL
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

    def __init__(self, rating, comment, created_at, price):
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return '' % self.id



db.create_all()
