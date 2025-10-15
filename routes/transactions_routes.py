from flask import request, jsonify, Blueprint
from flask_login import login_required

from services.transaction_services import (
    create_transaction,
    get_balance,
    import_transactions_json,
    get_transactions,
    export_transactions_json,
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


@transactions_bp.route("/add/import", methods=["POST"])
@login_required
def import_transactions():
    file = request.files["file"]

    response, status = import_transactions_json(file)

    return jsonify(response), status


@transactions_bp.route("/", methods=["GET"])
@login_required
def transactions():
    response, status = get_transactions()

    return jsonify(response), status


@transactions_bp.route("/balance", methods=["GET"])
@login_required
def transactions_balance():
    response, status = get_balance()

    return jsonify(response), status


@transactions_bp.route("/export", methods=["GET"])
@login_required
def export_transactions():
    response, status = export_transactions_json()

    return response, status


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
