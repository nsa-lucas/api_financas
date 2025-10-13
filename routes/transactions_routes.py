from flask import request, jsonify, Blueprint
from flask_login import login_required

from services.transaction_services import (
    create_transaction,
    get_transactions,
    transaction_update,
    transaction_delete,
)

transactions_bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")


@transactions_bp.route("/add", methods=["POST"])
@login_required
def add_transactions():
    data = request.json

    response, status = create_transaction(data)

    return jsonify(response), status


@transactions_bp.route("/", methods=["GET"])
@login_required
def transactions():
    response, status = get_transactions()

    return jsonify(response), status


@transactions_bp.route("/update/<int:transaction_id>", methods=["PUT"])
@login_required
def update_transaction(transaction_id):
    data = request.json

    response, status = transaction_update(data, transaction_id)

    return jsonify(response), status


@transactions_bp.route("/delete/<int:transaction_id>", methods=["DELETE"])
@login_required
def delete_transaction(transaction_id):
    response, status = transaction_delete(transaction_id)

    return jsonify(response), status
