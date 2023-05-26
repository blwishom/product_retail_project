from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from model import db, Customer, Product, Order, Review, order_product
#from forms.customer_form import LoginForm
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

with app.app_context():
    db.create_all()

#LOGIN/MAIN

@app.route('/')
def landing_page():
    return render_template('landing.html')

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

#review landing page/how-to
@app.route('/reviews/')
def reviews():
    return 'reviews/view: view all reviews || reviews/search?q=(keyword): search by product name or reviewer username || reviews/add: create a review || /reviews/(review id): update an existing review'

#creating a customer review on a product
@app.route('/reviews/add', methods=['POST'])
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
@app.route('/reviews/view', methods=['GET'])
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

#product landing page/how-to
@app.route('/products/')
def products():
    return render_template('products.html')

@app.route('/products/view')
def view_products():
    return render_template('view_products.html')

@app.route('/products/view/search')
def search_product():
    return render_template('search_product.html')

# Update a product record
@app.route('/products/update', methods=['GET', 'POST'])
def render_update_product_form():
    success_message = None

    if request.method == 'POST':
        # Process the form data and update the product in the database
        # ...

        # Set the success message
        success_message = 'Product updated successfully'

        # Redirect back to the update page
        return redirect('/products/update')

    return render_template('update_product.html', success_message=success_message)

@app.route('/products/delete', methods=['GET', 'DELETE', 'POST'])
def render_delete_product():
    return render_template('delete_product.html')


@app.route('/products/created')
def product_created():
    return 'Product created successfully!'

@app.route('/products/added', methods=['POST'])
def create_product():
    product_name = request.form['product_name']
    product_desc = request.form['product_desc']
    in_stock = request.form['in_stock']
    product_price = request.form['product_price']
    product_category = request.form['product_category']
    product_brand = request.form['product_brand']
    updated_at = datetime.datetime.now()

    product = Product(
        
        product_name=product_name,
        product_desc=product_desc,
        in_stock=in_stock,
        product_price=product_price,
        product_category=product_category,
        product_brand=product_brand,
        updated_at=updated_at
    )
    db.session.add(product)
    db.session.commit()

    # Retrieve the success message from the form data
    success_message = request.form.get('success_message')

    return render_template('product_created.html', success_message=success_message)


@app.route('/products/add', methods=['GET', 'POST'])
def render_add_product_form():
    if request.method == 'POST':
        return create_product()
    else:
        return render_template('add_product.html')

#View products
@app.route('/products/view/sortby=<string:category>/', methods=['GET'])
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
                           'product_brand': result.product_brand,
                           'updated_at': result.updated_at} for result in results]

    return jsonify(serialized_results)

#search products
@app.route('/products/view/search/display', methods=['GET'])
def search_products():
    # Get the search query from the request parameters
    search_query = request.args.get('q', '')

    # Perform the search query on the Product model
    products = Product.query.filter(
        or_(
            Product.product_name.ilike(f'%{search_query}%'),
            Product.product_desc.ilike(f'%{search_query}%'),
            Product.product_category.ilike(f'%{search_query}%'),
            Product.product_brand.ilike(f'%{search_query}%')
        )
    ).all()

    # Serialize the products into a JSON response
    product_list = []
    for product in products:
        product_data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_desc': product.product_desc,
            'in_stock': product.in_stock,
            'product_price': product.product_price,
            'product_category': product.product_category,
            'product_brand': product.product_brand,
            'updated_at': product.updated_at
        }
        product_list.append(product_data)

    return jsonify({'products': product_list})


# Update a product record
@app.route('/products/update/updating', methods=['POST'])
def update_product():
    # Retrieve the product ID from the request data
    product_id = request.form.get('product_id')
    
    # Retrieve the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Update the product attributes based on the request data
    product.product_name = request.form.get('product_name')
    product.product_desc = request.form.get('product_desc')
    product.in_stock = request.form.get('in_stock')
    product.product_price = request.form.get('product_price')
    product.product_category = request.form.get('product_category')
    product.product_brand = request.form.get('product_brand')
    product.updated_at = datetime.datetime.now()
        
     # Save the changes to the database
    try:
        
        db.session.commit()
        return redirect(url_for('update_success'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating product', 'error': str(e)}), 500

@app.route('/products/update/success')
def update_success():
    return render_template('update_success.html')


@app.route('/products/delete/deleting', methods=['DELETE', 'POST'])
def delete_product():
    # Retrieve the product ID from the request data
    product_id = request.form.get('product_id')

    # Retrieve the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('delete_success'))

@app.route('/products/delete/success')
def delete_success():
    return render_template('delete_success.html')

if __name__ == "__main__":
    app.run(debug=True)
  
    
    