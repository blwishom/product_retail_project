from flask import Flask
from flask import Blueprint, jsonify
from flask_login import login_required


app = Flask(__name__)
customer_routes = Blueprint('customers', __name__)


# @app.route('/login')
# # @login_required
# def customers():
#     # customers = Customer.query.all()
#     # return {'customers': [customer.to_dict() for customer in customers]}
#     return 'Hello'


@customer_routes.route('/<int:id>')
@login_required
def customer(id):
    customer = Customer.query.get(id)
    return customer.to_dict()

if __name__ == "__main__":
    app.run(debug=True)
