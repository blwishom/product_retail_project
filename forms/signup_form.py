from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from model import Customer


def user_exists(form, field):
    email = field.data
    customer = Customer.query.filter(Customer.email == email).first()
    if customer:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    username = field.data
    customer = Customer.query.filter(Customer.username == username).first()
    if customer:
        raise ValidationError('Username is already in use.')


class SignUpForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), username_exists])
    email = StringField('email', validators=[DataRequired(), user_exists])
    password = StringField('password', validators=[DataRequired()])
