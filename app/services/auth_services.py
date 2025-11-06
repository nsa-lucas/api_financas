from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash


from app.models.user import User


def auth(data):
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


def protected():
    current_user = get_jwt_identity()

    user = User.query.get(current_user)

    if user:
        return ({"email": user.email, "name": user.name}, 200)

    return {"message": "User not found"}, 404
