from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.models.user import User
from app.services.user_services import (
    create_user,
    user_login,
    delete_user_all,
    update_user_data,
)

from app.extensions import blacklist

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/signup", methods=["POST"])
def create_user_route():
    data = request.json

    response, status = create_user(data)

    return jsonify(response), status


@users_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user_route():
    data = request.json

    response, status = delete_user_all(data)

    return jsonify(response), status


@users_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_user_route():
    data = request.json

    response, status = update_user_data(data)

    return jsonify(response), status


@users_bp.route("/signin", methods=["POST"])
def login():
    data = request.json

    response, status = user_login(data)

    return jsonify(response), status


@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    user = User.query.get(current_user)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {"message": "Token accepted", "user": {"userId": user.id, "email": user.email}}
    ), 200


@users_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "Exiting..."})
