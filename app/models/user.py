from flask_login import UserMixin
import uuid

from app.extensions import db, jwt


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    transactions = db.relationship(
        "Transaction", backref="user", lazy=True, cascade="all, delete"
    )  # lazy=true só recupera as informações de transações quando for requisitado
    categories = db.relationship(
        "Category", backref="user", lazy=True, cascade="all, delete"
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())


@jwt.user_lookup_loader
def load_user(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)
