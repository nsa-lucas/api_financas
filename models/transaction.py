from extensions import db


class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(60), nullable=False)
  value = db.Column(db.Float, nullable=False)
  type = db.Column(db.String(7), nullable=False)
  date = db.Column(db.Date, nullable=False)
