from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String(50))
  l_name = db.Column(db.String(50))
  username = db.Column(db.String(50), unique=True)
  email = db.Column(db.String(255), unique=True)
  password_hash = db.Column(db.String(128))
  admin = db.Column(db.Boolean, default=False)

  def __repr__(self):
    return "<User {}: {} {}>".format(self.username, self.f_name, self.l_name)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  image = db.Column(db.String(255), default='http://placehold.it/800x800')
  price = db.Column(db.Float)
  inventory = db.Column(db.Integer)


@login.user_loader
def load_user(id):
  return User.query.get(int(id))