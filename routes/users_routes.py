from flask import request, jsonify, Blueprint
from flask_login import login_required, logout_user

from services.user_services import (
    create_user,
    user_login,
    delete_user_all,
    update_user_data,
)

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/add", methods=["POST"])
def add_user():
    data = request.json

    response, status = create_user(data)

    return jsonify(response), status


# ROTA PARA DELETAR USUARIO
# OBS>> AO DELETAR UM USUARIO, DEVE-SE DELETAR TAMBÉM TODAS AS TRANSAÇÕES E CATEGORIAS DESSE USUARIO
@users_bp.route("/delete", methods=["DELETE"])
@login_required
def delete_user():
    data = request.json

    response, status = delete_user_all(data)

    return jsonify(response), status


@users_bp.route("/update", methods=["PUT"])
@login_required
def update_user():
    data = request.json

    response, status = update_user_data(data)

    return jsonify(response), status


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    response, status = user_login(data)

    return jsonify(response), status


@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    return jsonify({"message": "Exiting..."})
