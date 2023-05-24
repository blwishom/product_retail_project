from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://<mysql_username>:<mysql_password>@<mysql_host>:<mysql_port>/<mysql_db>'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = "Product"
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
db.create_all()