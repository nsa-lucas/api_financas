from flask import send_file
import json
from io import BytesIO
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import func, desc, extract
from datetime import datetime


from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction
from app.services.category_services import create_category
from app.schemas.transaction_schema import (
    transaction_schema,
    transactions_schema,
)
from app.schemas.filter_transactions_schema import filter_transaction_schema
from app.utils.to_datetime import to_datetime


def create_transaction(data):
    current_user = get_jwt_identity()

    data["user_id"] = current_user

    if data.get("date"):
        data["date"] = to_datetime(data["date"]).date()

    category = create_category(data.get("category"))
    data["category_id"] = data.pop("category")
    data["category_id"] = category.id

    data["description"] = data["description"].lower()
    data["type"] = data["type"].strip().lower()

    try:
        validated_data = transaction_schema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    validated_data["amount"] = round(validated_data["amount"], 2)

    transaction = Transaction(**validated_data)

    db.session.add(transaction)
    db.session.commit()

    return {
        "message": "Transaction added successfully",
    }, 201


def import_transactions_json(file):
    current_user = get_jwt_identity()

    if file.content_type != "application/json":
        return {"message": "Invalid json file"}, 400

    transactions_json = json.load(file)

    for item in transactions_json:

        item["user_id"] = current_user

        if item.get("date"):
            item["date"] = to_datetime(item["date"]).date()

        category = create_category(item.get("category"))

        item["category_id"] = item.pop("category")

        item["category_id"] = category.id

        transaction_replace = {
            "user_id": item["user_id"],
            "description": item["description"],
            "amount": item["amount"],
            "category_id": item["category_id"],
            "type": item["type"],
            "date": item["date"],
        }

        try:
            validated_data = transaction_schema.load(transaction_replace)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        transaction = Transaction(**validated_data)

        db.session.add(transaction)

    db.session.commit()

    return {"message": "Transactions list import successfully"}, 201


def movement_summary(params):
    current_user = get_jwt_identity()

    transactions = Transaction.query.filter(Transaction.user_id == current_user)

    if len(transactions.all()) == 0:
        return ({"message": "Transactions not found"}), 404

    try:
        filter_params = filter_transaction_schema.load(params)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    if filter_params["order_by_date"] == "asc":
        transactions = transactions.order_by(Transaction.date.asc())

    else:
        transactions = transactions.order_by(Transaction.date.desc())

    if filter_params["order_by_amount"] == "asc":
        transactions = transactions.order_by(Transaction.amount.asc())

    if filter_params["order_by_amount"] == "desc":
        transactions = transactions.order_by(Transaction.amount.desc())

    if (
        filter_params["category_name"]
        and len(filter_params["category_name"].strip().lower()) != 0
    ):
        category_name = filter_params["category_name"]

        transactions = transactions.join(Category).filter(
            Category.name.ilike(f"%{category_name}%")
        )

    transactions_filtered = transactions.paginate(
        page=filter_params["page"], per_page=filter_params["limit"], max_per_page=100
    )

    return transactions_schema.dump(transactions_filtered), 200


def get_expenses(params):

    current_user = get_jwt_identity()

    month = params.get("month", type=int)
    year = params.get("year", type=int)
    limit = params.get("limit", 3, type=int)
    type = params.get("type", type=str)

    if not year or len(str(year)) != 4:  # SE NAO HOUVER UM ANO OU LENGTH(ANO) != 4
        year = datetime.now().year  # ANO IGUAL AO ANO ATUAL

    if not (
        isinstance(month, int) and 1 <= month <= 12
    ):  # SE MES FOR MENOR QUE 1 OU MAIOR QUE 12
        month = datetime.now().month  # MES IGUAL MES ATUAL

    if type != "expense" and type != "income" and not type:
        type = "expense"

    get_expenses = (
        Transaction.query.join(Category)
        .filter(Transaction.user_id == current_user, Transaction.type == type)
        .with_entities(Category.name, func.sum(Transaction.amount).label("total"))
    )

    if month:
        get_expenses = get_expenses.filter(extract("month", Transaction.date) == month)

    if year:
        get_expenses = get_expenses.filter(extract("year", Transaction.date) == year)

    get_expenses = (
        get_expenses.group_by(Category.name).order_by(desc("total")).limit(limit).all()
    )
    # FILTRO DE CATEGORIAS COM MAIORES GASTOS - PER MONTH, PER YEAR
    res_expenses = [
        {"category": name, "total": round(float(total), 2)}
        for name, total in get_expenses
    ]

    return res_expenses, 200


def export_transactions_json():
    current_user = get_jwt_identity()

    transactions = Transaction.query.filter(Transaction.user_id == current_user).all()

    if len(transactions) == 0:
        return ({"message": "Transactions not found"}), 404

    all_transactions = transactions_schema.dump(transactions)

    # Gera JSON formatado
    json_data = json.dumps(all_transactions, ensure_ascii=False, indent=2)

    # Cria arquivo em memória
    buffer = BytesIO()
    buffer.write(json_data.encode("utf-8"))
    buffer.seek(0)

    filename = "transactions_export.json"

    return (
        send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="application/json",
        ),
        200,
    )


def transaction_update(data, transaction_id):
    current_user = get_jwt_identity()

    if not data:
        return {"message": "No data changed"}, 400

    transaction = Transaction.query.filter(
        Transaction.user_id == current_user, Transaction.id == transaction_id
    ).first()

    if not transaction:
        return {"message": "Transaction not found"}, 404

    if data.get("date"):
        data["date"] = to_datetime(data["date"]).date()
        transaction.date = data["date"]

    if data.get("category"):
        category = create_category(data.get("category"))
        transaction.category_id = category.id

    if data.get("description"):
        transaction.description = data["description"].lower()

    if data.get("amount"):
        transaction.amount = round(data["amount"], 2)

    if data.get("type"):
        t = data["type"].strip().lower()
        if t not in ["income", "expense"]:
            return {"message": "Invalid type. Must be 'income' or 'expense'."}, 400
        transaction.type = t

    db.session.commit()

    return {"message": "Transaction updated successfully"}, 200


def transaction_delete(transaction_id):
    current_user = get_jwt_identity()

    transaction = Transaction.query.filter(
        Transaction.id == transaction_id, Transaction.user_id == current_user
    ).first()

    if transaction:
        db.session.delete(transaction)
        db.session.commit()

        return {"message": "Transaction deleted successfully"}, 200

    return {"message": "Transaction not found"}, 404
