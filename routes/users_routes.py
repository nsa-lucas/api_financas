from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from models.User import User
from services.user_services import (
    create_user,
    user_login,
    delete_user_all,
    update_user_data,
)

from extensions import blacklist

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/add", methods=["POST"])
def add_user():
    data = request.json

    response, status = create_user(data)

    return jsonify(response), status


# ROTA PARA DELETAR USUARIO
# OBS>> AO DELETAR UM USUARIO, DEVE-SE DELETAR TAMBÉM TODAS AS TRANSAÇÕES E CATEGORIAS DESSE USUARIO
@users_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    data = request.json

    response, status = delete_user_all(data)

    return jsonify(response), status


@users_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_user():
    data = request.json

    response, status = update_user_data(data)

    return jsonify(response), status


@users_bp.route("/login", methods=["POST"])
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
