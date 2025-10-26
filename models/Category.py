from extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    transactions = db.relationship("Transaction", backref="category", lazy=True)
