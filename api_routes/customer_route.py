# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from ..model import Customer
# import datetime

# @app.route('/')
# def landing_page():
#     return 'product retail landing page'

# @app.route('/signup')
# def signup():
#     return 'customer signup route'

# @app.route('/login')
# def login():
#     customers = Customer.query.all()
#     return 'customer login route'

# @app.route('/customer/<int:id>/')
# # @login_required
# def customer(id):
#     customers = Customer.query.all()
#     return 'customer id route'


# if __name__ == "__main__":
#     app.run(debug=True)
