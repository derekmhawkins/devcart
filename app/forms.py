from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User, Product

class LoginForm(FlaskForm):
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember_me = BooleanField("Remember Me")
  submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
  f_name = StringField("First Name", validators=[DataRequired()])
  l_name = StringField("Last Name", validators=[DataRequired()])
  username = StringField("Username", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField("Register")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use different email address')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use different username')

class ProductForm(FlaskForm):
  name = StringField("Product Name", validators=[DataRequired()])
  image = FileField("Product Image")
  price = DecimalField("Product Price", validators=[DataRequired()], places=2)
  inventory = IntegerField("Inventory", validators=[DataRequired()])
  submit = SubmitField("Add Product")

  def validate_name(self, name):
    product = Product.query.filter_by(name=name.data).first()
    if product is not None:
      raise ValidationError("Product already exists")