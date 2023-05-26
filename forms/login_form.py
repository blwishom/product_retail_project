from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from model import Customer

def customer_exists(form, field):
    email = field.data
    customer = Customer.query.filter(Customer.email == email).first()
    if not customer:
        raise ValidationError('Email provided was not found.')


def password_matches(form, field):
    password = field.data
    username = form.data['username']
    customer = Customer.query.filter(Customer.username == username).first()
    if not customer:
        raise ValidationError('No account exists with this username.')
    if not customer.check_password(password):
        raise ValidationError('Password was incorrect please renter.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), password_matches])
    submit = SubmitField('Login')
