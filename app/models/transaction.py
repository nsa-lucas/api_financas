from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(7), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
