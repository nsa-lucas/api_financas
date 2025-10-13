from flask_login import UserMixin

from extensions import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    transactions = db.relationship(
        "Transaction", backref="user", lazy=True, cascade="all, delete"
    )  # lazy=true só recupera as informações de transações quando for requisitado
    categories = db.relationship(
        "Category", backref="user", lazy=True, cascade="all, delete"
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
