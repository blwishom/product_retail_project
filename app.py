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




if __name__ == "__main__":
    app.run(debug=True)
