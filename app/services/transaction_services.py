from flask import send_file
import json
from io import BytesIO
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError


from app.extensions import db
from app.utils.to_datetime import to_datetime
from app.services.category_services import create_category
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction_schema import transaction_schema, transactions_schema
from app.schemas.filter_transactions_schema import filter_transaction_schema


def create_transaction(data):
    current_user = get_jwt_identity()

    data["user_id"] = current_user

    if data.get("date"):
        data["date"] = to_datetime(data["date"]).date()

    category = create_category(data.get("category"))

    data["category_id"] = data.pop("category")

    data["category_id"] = category.id

    try:
        validated_data = transaction_schema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

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
        if not all(
            [
                item.get("description")
                and item.get("amount")
                and item.get("type")
                and item.get("date")
                and item.get("category_name")
            ]
        ):
            return {"message": "Invalid json items"}, 400

        category_id = create_category(item["category_name"])

        transaction_type = item["type"].strip().lower()

        if transaction_type != "receita" and transaction_type != "despesa":
            return {"message": "Invalid transaction type data"}, 400

        transaction = Transaction(
            description=item["description"],
            amount=round(item["amount"], 2),
            type=transaction_type,
            date=item["date"],
            user_id=current_user,
            category_id=category_id,
        )

        db.session.add(transaction)

    db.session.commit()

    return {"message": "Transactions list import successfully"}, 201


def get_transactions(params):
    current_user = get_jwt_identity()

    transactions = Transaction.query.filter(Transaction.user_id == current_user)

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
        page=filter_params["page"], per_page=filter_params["limit"], max_per_page=20
    )

    return transactions_schema.dump(transactions_filtered), 200


def export_transactions_json():
    current_user = get_jwt_identity()

    transactions = Transaction.query.filter(Transaction.user_id == current_user).all()

    if not transactions:
        return ({"message": "Transactions not found"}), 404

    all_transactions = [
        {
            "description": t.description,
            "amount": round(t.amount, 2),
            "type": t.type,
            "date": t.date.strftime("%d-%m-%Y"),
            "category_name": t.category.name,
        }
        for t in transactions
    ]

    # Gera JSON formatado
    json_data = json.dumps(all_transactions, ensure_ascii=False, indent=2)

    # Cria arquivo em memória
    buffer = BytesIO()
    buffer.write(json_data.encode("utf-8"))
    buffer.seek(0)

    filename = "transactions_export.json"

    return send_file(
        buffer, as_attachment=True, download_name=filename, mimetype="application/json"
    ), 200


def transaction_update(data, transaction_id):
    current_user = get_jwt_identity()

    if not data:
        return {"message": "No data changed"}, 400

    transaction = Transaction.query.filter(
        Transaction.id == transaction_id, Transaction.user_id == current_user
    ).first()  # RETORNA TRANSAÇÃO DO USUARIO LOGADO

    # VERIFICANDO SE TRANSAÇÃO EXISTE
    if transaction:
        # VERIFICA SE O USUARIO PASSOU UMA NOVO NOME PARA CATEGORIA E O NOME É DIFERENTE DO ATUAL
        if (
            data.get("category_name")
            and data.get("category_name") != transaction.category.name
        ):
            # SE TRUE, CHAMA A FUNCAO GET_CATEOGORY, ONDE SERA REQUISITADO OU CRIADO A NOVA CATEGORIA
            category_id = create_category(data.get("category_name"))

        else:
            # SE FALSE, RETORNA O ID DA CATEGORIA ATUAL
            category_id = transaction.category_id

        transaction.description = data.get("description", transaction.description)
        transaction.amount = round(data.get("amount", transaction.amount), 2)
        transaction.type = data.get("type", transaction.type)
        transaction.date = data.get("date", transaction.date)
        transaction.category_id = category_id

        db.session.commit()

        return {"message": "Transaction updated successfully"}, 200

    return {"message": "Transaction not found"}, 404


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
