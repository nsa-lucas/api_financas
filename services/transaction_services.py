from flask import send_file
from flask_login import current_user
from sqlalchemy import extract, func
import json
from io import BytesIO
import calendar

from extensions import db
from models.Transaction import Transaction
from .category_services import get_category


def create_transaction(data):
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
            user_id=current_user.id,
            category_id=category_id,
        )

        db.session.add(transaction)
        db.session.commit()

        return {"message": "Transaction added successfully"}, 201

    return {"message": "Invalid transaction data"}, 400


def import_transactions_json(file):
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
            user_id=current_user.id,
            category_id=category_id,
        )

        db.session.add(transaction)

    db.session.commit()

    return {"message": "Transactions list import successfully"}, 201


def get_transactions():
    transactions = (
        Transaction.query.order_by(Transaction.date.desc())
        .filter(Transaction.user_id == current_user.id)
        .all()
    )

    if not transactions:
        return ({"message": "Transactions not found"}), 404

    all_transactions = [
        {
            "id": t.id,
            "description": t.description,
            "amount": round(t.amount, 2),
            "type": t.type,
            "date": t.date,
            "user_id": t.user_id,
            "category_name": t.category.name,
            "category_id": t.category.id,
        }
        for t in transactions
    ]

    return {"Transações": all_transactions}, 200


def get_balance():
    total_balance = (
        db.session.query(
            extract("year", Transaction.date).label("year"),
            extract("month", Transaction.date).label("month"),
            func.sum(Transaction.amount)
            .filter(
                Transaction.user_id == current_user.id, Transaction.type == "despesa"
            )
            .label("total_expense"),
            func.sum(Transaction.amount)
            .filter(
                Transaction.user_id == current_user.id, Transaction.type == "receita"
            )
            .label("total_income"),
        )
        .group_by(
            extract("year", Transaction.date),
            extract("month", Transaction.date),
        )
        .order_by(extract("year", Transaction.date), extract("month", Transaction.date))
    )

    result = [
        {
            "Ano": int(b.year),
            "Mês": calendar.month_name[int(b.month)],
            "Despesas do mês": round((b.total_expense or 0), 2),
            "Receita do mês": round((b.total_income or 0), 2),
            "Saldo atual": round((b.total_income or 0) - (b.total_expense or 0), 2),
        }
        for b in total_balance
    ]

    return result, 200


def export_transactions_json():
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id
    ).all()

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
    if not data:
        return {"message": "No data changed"}, 400

    transaction = Transaction.query.filter(
        Transaction.id == transaction_id, Transaction.user_id == current_user.id
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
    transaction = Transaction.query.filter(
        Transaction.id == transaction_id, Transaction.user_id == current_user.id
    ).first()

    if transaction and transaction.user_id == current_user.id:
        db.session.delete(transaction)
        db.session.commit()

        return {"message": "Transaction deleted successfully"}, 200

    return {"message": "Transaction not found"}, 404
