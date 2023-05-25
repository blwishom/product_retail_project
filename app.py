from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Customer, Product, Order, Review, order_product
import datetime
from sqlalchemy import or_

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

#creating a customer review on a product
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    customer_id = data['customer_id']
    product_id = data['product_id']
    rating = data['rating']
    comment = data['comment']
    created_at = datetime.datetime.now()

    review = Review(
        customer_id=customer_id,
        product_id=product_id,
        rating=rating,
        comment=comment,
        created_at=created_at
        )
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review created successfully'}), 201

# viewing all customer reviews
@app.route('/reviews', methods=['GET'])
def view_reviews():
    reviews = Review.query.all()
    review_list = []
    for review in reviews:
        review_data = {
            'review_id': review.review_id,
            'customer_id': review.customer_id,
            'product_id': review.product_id,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at
        }
        review_list.append(review_data)
    
    return jsonify({'reviews': review_list}), 200


@app.route('/reviews/search', methods=['GET'])
def search_reviews():
    search_query = request.args.get('q', '') 
    results = Review.query.filter(or_(Review.customer.has(Customer.username.ilike(f'%{search_query}%')),
                                      Review.product.has(Product.product_name.ilike(f'%{search_query}%')))).all()
    
    serialized_results = [{'review_id': result.review_id,
                       'customer_id': result.customer_id,
                       'product_id': result.product_id,
                       'rating': result.rating,
                       'comment': result.comment,
                       'created_at': result.created_at} for result in results]
    
    return jsonify(serialized_results)




with app.app_context():
    db.create_all()
    
    customer1 = Customer(first_name="Sherwin",
                        last_name="Manchester",
                        username="sherman",
                        email= "smanchester@gmail.com",
                        address="222 Plum Ln Pocatello, Id",
                        hashed_password= "stheman")
    
    customer2 = Customer(first_name="Carlo",
                        last_name="Morrison",
                        username="cmorrison",
                        email= "cmorrison101@gmail.com",
                        address="367 Ranger Ct Ruidoso, Nm",
                        hashed_password= "pass12345")
    
    customer3 = Customer(first_name="Neve",
                        last_name="Reilly",
                        username="catluvr234",
                        email= "catluvr234@gmail.com",
                        address="473 Opal Ave Oxford, Mi",
                        hashed_password= "calicotabby4")
    
    customer4 = Customer(first_name="Zane",
                        last_name="Hester",
                        username="coppiceintoned",
                        email= "coppiceintoned@gmail.com",
                        address="777 Oracle Blvd Herkimer, Ny",
                        hashed_password= "uG7q9PL8")
    
    customer5 = Customer(first_name="Ellis",
                        last_name="Knoxx",
                        username="guitarrh3ro@gmail.com",
                        email= "gh3roknoxx@gmail.com",
                        address="894 Rayhan Rd Dayton, Tn",
                        hashed_password= "helloflask!")
    
    product1 = Product(product_name="Oversized Chicago Bulls 6 Rings T-Shirt",
                        product_desc="Images from the Chicago Bulls final championship during their dynamic run of winning 6 NBA championships in the 90s.",
                        in_stock=10,
                        product_price= 24.99,
                        product_category="Shirts",
                        )

    product2 =   Product(product_name = "T-Shirt",
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
    '''
    for data in order_product_data:
        db.session.execute(order_product.insert().values(data))

    
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.add(customer4)
    db.session.add(customer5)

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(order)
    db.session.add(review)

    db.session.commit()
    '''
if __name__ == "__main__":
    app.run(debug=True)