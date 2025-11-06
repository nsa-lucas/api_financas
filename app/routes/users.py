from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from app.services.user_services import (
    create_user,
    delete_user_all,
    update_user_data,
)


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
