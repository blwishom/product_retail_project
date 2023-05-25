from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from model import db, Customer, Product, Order, Review, order_product
from forms.customer_form import LoginForm
import datetime
import secrets
from sqlalchemy import or_
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_retail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

#LOGIN/MAIN

@app.route('/')
def landing_page():
    return 'product retail landing page'

@app.route('/signup')
def signup():
    return 'customer signup route'

@app.route('/login')
def get_csrf_token():
    # Generates CSRF token
    csrf_token = generate_csrf()
    response = jsonify({'csrf_token': csrf_token})
    response.set_cookie('csrf_token', csrf_token, secure=True, httponly=True, samesite='Strict')
    return response
def login():
    # Logs a user in
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = Customer.query.filter(Customer.email == form.data['email']).first()
        form.login_user(user)
        return user.to_dict()
    return {'errors': 'validation_errors_to_error_messages' (form.errors)}, 401

#CUSTOMER

@app.route('/customer')
def customer():
    customers = Customer.query.all()
    customer_dict = {'customers': [customer.to_dict() for customer in customers]}
    return customer_dict

@app.route('/customer/<int:id>/')
# @login_required
def customer_home(id):
    customers = Customer.query.all()
    return 'customer id route'

#REVIEW

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
                       'created_at': result.created_at,
                       'updated_at': result.updated_at} for result in results]
    
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

#PRODUCTS

#Make a product
@app.route('/products/add', methods=['POST'])
def create_product():

    data = request.get_json()
    product_id = data['product_id']
    product_name = data['product_name']
    product_desc = data['product_desc']
    in_stock = data['in_stock']
    product_price = data['product_price']
    product_category = data['product_category']
    product_brand = data['product_brand']

    product = Product(
        product_id = product_id,
        product_name = product_name,
        product_desc = product_desc,
        in_stock = in_stock,
        product_price = product_price,
        product_category = product_category,
        product_brand = product_brand
        )
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'}), 201

#redirect from an empty input?
@app.route('/products/add')
def create_product_info():
    return "To enter a product, send a JSON object with the following items: product_id, product_name, product_desc, in_stock, product_price, product_category, product_brand"

#View products
@app.route('/products/sortby=<string:category>/')
def product_sort(category):

    match(category):
        case "id":
            results = db.session.execute(db.select(Product).order_by( desc("product_id"))).scalars()
            
        case "stock":
            results = db.session.execute(db.select(Product).order_by( desc("in_stock"))).scalars()
            
        case "price":
            results = db.session.execute(db.select(Product).order_by( desc("product_price"))).scalars()

        case _ :
            return "invalid query!"
        
    # Serialize the results into a list of dictionaries
    serialized_results = [{'product_id': result.product_id,
                           'product_name': result.product_name,
                           'in_stock': result.in_stock,
                           'product_price': result.product_price,
                           'product_desc' : result.product_desc,
                           'product_category': result.product_category,
                           'product_brand': result.product_brand} for result in results]

    return jsonify(serialized_results)

@app.route('/products/')
def products():
    return 'products/sortby=category: view all products by product id (category=id), quantity in stock (category=stock), or price (price) | products/add: add a product to the catalogue'

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
    
#DELETE A PRODUCT
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Retrieve the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Delete the product from the database
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting product', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
  
    
    