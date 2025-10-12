from flask_login import current_user

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

        if data["type"] != "receita" and data["type"] != "despesa":
            return {"message": "Invalid transaction type data"}, 400

        transaction = Transaction(
            description=data["description"],
            amount=data["amount"],
            type=data["type"],
            date=data["date"],
            user_id=current_user.id,
            category_id=category_id,
        )

        db.session.add(transaction)
        db.session.commit()

        return {"message": "Transaction added successfully"}, 201

    return {"message": "Invalid transaction data"}, 400


def get_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    if not transactions:
        return ({"message": "Transactions not found"}), 404

    all_transactions = [
        {
            "id": t.id,
            "description": t.description,
            "amount": t.amount,
            "type": t.type,
            "date": t.date,
            "user_id": t.user_id,
            "category_name": t.category.name,
            "category_id": t.category.id,
        }
        for t in transactions
    ]

    return all_transactions, 200


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
        transaction.amount = data.get("amount", transaction.amount)
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
