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


# viewing all products
@app.route('/products', methods=['GET'])
def view_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_desc': product.product_desc,
            'in_stock': product.in_stock,
            'product_price': product.product_price,
            'product_category': product.product_category,
            'product_brand': product.product_brand
        }
        product_list.append(product_data)
    
    return jsonify({'products': product_list}), 200

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

# Update a review record
@app.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    # Retrieve the review from the database
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'message': 'Review not found'}), 404

    # Update the review attributes based on the request data
    data = request.get_json()
    if 'rating' in data:
        review.rating = data['rating']
    if 'comment' in data:
        review.comment = data['comment']
    if 'customer_id' in data:
        review.customer_id = data['customer_id']
    if 'product_id' in data:
        review.product_id = data['product_id']
    review.updated_at = datetime.datetime.now()
    
    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Review updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating review', 'error': str(e)}), 500

# Update a product record
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Retrieve the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Update the product attributes based on the request data
    data = request.get_json()
    if 'product_name' in data:
        product.product_name = data['product_name']
    if 'product_desc' in data:
        product.product_desc = data['product_desc']
    if 'in_stock' in data:
        product.in_stock = data['in_stock']
    if 'product_price' in data:
        product.product_price = data['product_price']
    if 'product_category' in data:
        product.product_category = data['product_category']
    if 'product_brand' in data:
        product.product_brand = data['product_brand']

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating product', 'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
