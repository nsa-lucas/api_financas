from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError

from app.schemas.user_schema import user_schema
from app.extensions import db
from app.models.user import User


def create_user(data):
    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    email = data["email"].strip().lower()

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists."}, 409

    hashed_password = generate_password_hash(
        validated_data["password"], method="pbkdf2:sha256", salt_length=8
    )

    validated_data["password"] = hashed_password

    user = User(**validated_data)
    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201


# PARA DELETAR O USUARIO, DEVE SER DELETAR ANTES TODAS AS TRANSAÇÕES E CATEGORIAS DESSE USUARIO
def delete_user_all(data):
    user = User.query.get(get_jwt_identity().id)

    if check_password_hash(user.password, data["password"]):
        db.session.delete(user)
        db.session.commit()

        return {
            "User": "User deleted successfully. Exiting...",
        }, 200

    return {"message": "Invalid password"}, 400


def update_user_data(data):
    if not data:
        return {"message": "No data changed"}, 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    current_user = get_jwt_identity()

    user = User.query.get(current_user)

    if name:
        user.name = name

    if email:
        if User.query.filter(User.email == email).first():
            return {"message": "Email has already been used"}, 400
        user.email = email

    if password:
        if len(password) <= 8:
            return {"message": "Password must contain 8 characters or more"}, 400

        password_hashed = generate_password_hash(password, "pbkdf2:sha256", 8)

        user.password = password_hashed

    db.session.commit()

    return {"message": "User updated successfully"}, 200


def user_login(data):
    email = data["email"]

    user = User.query.filter(User.email == email).first()

    if not user:
        return {"message": "Email or password invalid"}, 400

    password_check = check_password_hash(user.password, data["password"])

    if password_check:
        token = create_access_token(identity=user.id)

        response = {"token": token, "user": {"id": user.id, "email": user.email}}

        return {"message": "Authorized login", "data": response}, 202

    return {"message": "Email or password invalid"}, 400
