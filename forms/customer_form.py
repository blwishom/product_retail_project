from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf


def customer_exists(form, field):
    # Checking if user exists
    email = field.data
    customer = Customer.query.filter(Customer.email == email).first()
    if not customer:
        raise ValidationError('Email provided was not found.')


def password_matches(form, field):
    # Checking if password matches
    password = field.data
    email = form.data['email']
    customer = Customer.query.filter(Customer.email == email).first()
    if not customer:
        raise ValidationError('No such account exists for this email.')
    if not user.check_password(password):
        raise ValidationError('Password was incorrect.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), customer_exists])
    password = StringField('password', validators=[
                           DataRequired(), password_matches])
