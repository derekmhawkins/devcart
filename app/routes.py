from app import app, db # from app package, import app variable
from flask import render_template, url_for, flash, redirect, request, session
from app.forms import LoginForm, RegistrationForm, ProductForm, CheckoutForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Product
from werkzeug.urls import url_parse
import os, random
from werkzeug.utils import secure_filename
import stripe
from app.stripe import stripe_keys


@app.route('/', methods=['GET', 'POST'])
def index():
  form = ProductForm()
  products = Product.query.all()
  context = {
    "name": "Derek",
    "title": "Home",
    "form": form,
    "products": products
  }
  if form.validate_on_submit():
    basedir = os.path.abspath(os.path.dirname(__file__)) + '/static/products/uploads/'
    filename = ''.join([str(random.randint(0, 9)) for i in range(0, 9)]) + '.png'
    print(basedir + filename)
    if not os.path.exists(basedir):
      os.makedirs(basedir)
    product = Product(name=form.name.data, price=form.price.data, inventory=form.inventory.data)
    product.image = filename
    form.image.data.save(basedir + filename)
    flash("Product created!")
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template("index.html", **context)

@app.route('/delete_item/<int:id>')
def delete_item(id):
  session["cart"].remove(id)
  flash("Item removed from cart")
  return redirect(url_for('cart'))

@app.route('/add_to_cart/<int:id>')
def add_item(id):
  if "cart" not in session:
    session["cart"] = []
  session["cart"].append(id)
  flash("Item added to cart")
  return redirect(url_for('index'))

@app.route('/cart')
def cart():
  if "cart" not in session or "cart" is None:
    flash("There's nothing in your cart... yet")
    return render_template('cart.html', title='My Cart', display_cart={}, total=0)
  items = session["cart"]
  dict_of_items = {}
  totalPrice = 0
  for item in items:
    product = Product.query.get(item)
    totalPrice += product.price
    if product.id in dict_of_items:
      dict_of_items[product.id]["qty"] += 1
    else:
      dict_of_items[product.id] = {"id": product.id, "qty":1, "image":product.image, "name":product.name, "price":product.price}
  session["paymentTotal"] = totalPrice
  session["shopping_cart"] = dict_of_items
  return render_template("cart.html", display_cart=dict_of_items, total=totalPrice, title="My Cart")

@app.route('/checkout', methods=['GET'])
def checkout():
  context = {
    "title": "Checkout",
    "paymentTotal": session.get("paymentTotal", None),
    "form": CheckoutForm(),
    "key": stripe_keys['publishable_key'][2:]
  }
  amount = context['paymentTotal']
  return render_template('checkout.html', **context, amount=amount)


@app.route('/charge', methods=['GET ', 'POST'])
def charge():
  cart = session.get("cart", None)
  cart.clear()
  print(request.form)

  def convert_to_cents(dollar_amount):
    conversion = dollar_amount * 100
    # return "{:.2f}".format(conversion)
    return int(conversion)

  amount = session.get("paymentTotal", None)
  customer = stripe.Customer.create(
    email=request.form['stripeEmail'],
    source=request.form['stripeToken']
  )
  charge = stripe.Charge.create(
    customer=customer.id,
    amount=convert_to_cents(amount),
    currency='usd',
    description='Test Charge'
  )
  return render_template("charge.html", totalCharge=session.get("paymentTotal", None))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated: # If email/password, redirect to index page. 
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data): # If email/password incorrect, return error message
      flash("That's the wrong email or password. Try again!")
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data) # Otherwise, login the current user
    flash("You are logged in!")
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template("login.html", title="Log In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(f_name=form.f_name.data, l_name=form.l_name.data, username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash("Congratulations! You're registered.")
    login_user(user)
  return render_template('login.html', title="Register", form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html', title='Profile')
