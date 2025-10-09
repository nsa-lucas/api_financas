from flask_login import UserMixin
from extensions import db, login_manager

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(60), nullable=False)
  amount = db.Column(db.Float, nullable=False)
  type = db.Column(db.String(7), nullable=False)
  date = db.Column(db.Date, nullable=False)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  email = db.Column(db.String(120), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))