from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.User import User


def create_user(data):
    email = data["email"].strip().lower()

    # VERIFICANDO SE EMAIL JA EXISTE
    if User.query.filter_by(email=email).first():
        return {"message": "Email already exists"}, 409

    # CRIPTOGRAFANDO SENHA
    hashed_password = generate_password_hash(data["password"])

    user = User(name=data["name"], email=email, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return {"message": "User added successfully"}, 201


def user_login(data):
    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {"message": "Email or password invalid"}, 400

    password_check = check_password_hash(user.password, data["password"])

    if password_check:
        login_user(user)

        return {"message": "Authorized login"}, 202

    return {"message": "Email or password invalid"}, 400
