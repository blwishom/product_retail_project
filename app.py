from flask import Flask, jsonify, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from sqlalchemy import desc, or_
from model import db, Customer, Product, Review
from forms.login_form import LoginForm
from forms.signup_form import SignUpForm
import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_retail.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_SECRET_KEY'] = secrets.token_hex(16)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(customer_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'Product Retail Home Page'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_customer = Customer.query.filter_by(username=username).first()
        if existing_customer:
            return render_template('signup.html', error='Username is already taken')

        new_customer = Customer(username=username)
        new_customer.set_password(password)
        db.session.add(new_customer)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(username=form.username.data).first()
        if customer and customer.check_password(form.password.data):
            login_user(customer)
            return redirect('/')
        else:
            return 'Invalid username or password'

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


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
    return 'products/sortby=category: view all products by product id (category=id), quantity in stock (category=stock), or price (price) || products/add: add a product to the catalogue || products/(id): update an item (PUT) or delete an item (DELETE)'

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
    updated_at = datetime.datetime.now()


    product = Product(
        product_id = product_id,
        product_name = product_name,
        product_desc = product_desc,
        in_stock = in_stock,
        product_price = product_price,
        product_category = product_category,
        product_brand = product_brand,
        updated_at = updated_at
        )
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'}), 201
'''
#redirect from an empty input?
@app.route('/products/add')
def create_product_info():
    return "To enter a product, send a JSON object with the following items: product_id, product_name, product_desc, in_stock, product_price, product_category, product_brand"
'''
#View products
# @app.route('/products/sortby=<string:category>/')
# def product_sort(category):

#     match(category):
#         case "id":
#             results = db.session.execute(db.select(Product).order_by( desc("product_id"))).scalars()

#         case "stock":
#             results = db.session.execute(db.select(Product).order_by( desc("in_stock"))).scalars()

#         case "price":
#             results = db.session.execute(db.select(Product).order_by( desc("product_price"))).scalars()

#         case _ :
#             return "invalid query!"

#     # Serialize the results into a list of dictionaries
#     serialized_results = [{'product_id': result.product_id,
#                            'product_name': result.product_name,
#                            'in_stock': result.in_stock,
#                            'product_price': result.product_price,
#                            'product_desc' : result.product_desc,
#                            'product_category': result.product_category,
#                            'product_brand': result.product_brand,
#                            'updated_at': result.updated_at} for result in results]

#     return jsonify(serialized_results)

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
    product.updated_at = datetime.datetime.now()

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
