from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from services.category_services import (
    get_categories,
    create_category,
    update_category_name,
    delete_category_unused,
)

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@categories_bp.route("/", methods=["GET"])
@jwt_required()
def categories():
    response, status = get_categories()

    return jsonify(response), status


@categories_bp.route("/add", methods=["POST"])
@jwt_required()
def add_category():
    data = request.json

    response, status = create_category(data["category_name"])

    return jsonify(response), status


@categories_bp.route("/update/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    data = request.json

    response, status = update_category_name(data, category_id)

    return jsonify(response), status


@categories_bp.route("/delete/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    response, status = delete_category_unused(category_id)

    return jsonify(response), status
