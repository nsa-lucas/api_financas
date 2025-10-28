from flask import send_file
from sqlalchemy import extract
import json
from io import BytesIO
from flask_jwt_extended import get_jwt_identity


from extensions import db
from models.Category import Category
from models.Transaction import Transaction
from .category_services import get_category


def create_transaction(data):
    current_user = get_jwt_identity()

    if (
        data.get("description")
        and data.get("amount")
        and data.get("type")
        and data.get("date")
        and data.get("category_name")
    ):
        category_id = get_category(data["category_name"])

        transaction_type = data["type"].strip().lower()

        if transaction_type != "receita" and transaction_type != "despesa":
            return {"message": "Invalid transaction type data"}, 400

        transaction = Transaction(
            description=data["description"],
            amount=round(data["amount"], 2),
            type=transaction_type,
            date=data["date"],
            user_id=current_user,
            category_id=category_id,
        )

        db.session.add(transaction)
        db.session.commit()

        return {"message": "Transaction added successfully"}, 201

    return {"message": "Invalid transaction data"}, 400


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

        category_id = get_category(item["category_name"])

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

    page = params.get("page", type=int)
    limit = params.get("limit", type=int)
    category_name = params.get("category_name", type=str)
    transactions_type = params.get("type", type=str)
    transactions_year = params.get("year", type=str)
    # order_by_date = params.get("date_by_desc", type=str)
    order_by_amount = params.get("amount_by_desc", type=str)

    if not limit:
        limit = 8

    transactions_by_user = (
        Transaction.query.filter(Transaction.user_id == current_user)
        .order_by(Transaction.date.desc())
        .paginate(page=page, per_page=limit, max_per_page=15)
    )

    if order_by_amount == "desc":
        transactions_by_user = transactions_by_user.order_by(Transaction.amount.desc())

    if category_name:
        transactions_by_user = transactions_by_user.join(Category).filter(
            Category.name.ilike(f"%{category_name}%")
        )
    if transactions_type:
        transactions_by_user = transactions_by_user.filter(
            Transaction.type.ilike(f"%{transactions_type}%")
        )

    if transactions_year:
        transactions_by_user = transactions_by_user.filter(
            extract("year", Transaction.date) == transactions_year
        )

    if not transactions_by_user:
        return {"message": "Transactions not found"}, 404

    transactions = [
        {
            "id": t.id,
            "description": t.description,
            "amount": round(t.amount, 2),
            "type": t.type,
            "date": t.date.strftime("%d/%m/%Y"),
            "user_id": t.user_id,
            "category_name": t.category.name,
            "category_id": t.category.id,
        }
        for t in transactions_by_user
    ]

    return (transactions), 200


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
            category_id = get_category(data.get("category_name"))

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
