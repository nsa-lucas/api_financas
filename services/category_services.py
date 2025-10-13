from flask_login import current_user

from extensions import db
from models.Category import Category
from models.Transaction import Transaction


# CRIAÇÃO DE CATEGORIA PELA ROTA DE CATEGORIA
def create_category(category_name):
    # VERIFICANDO SE CATEGORIA JA EXISTE
    if Category.query.filter(
        Category.name == category_name, Category.user_id == current_user.id
    ).first():
        return {"message": "Category name already exists"}, 409

    category = Category(
        name=category_name.strip().lower(),  # transformando texto em caixa baixa
        user_id=current_user.id,
    )
    db.session.add(category)
    db.session.commit()

    return {"message": "Category created successfully"}, 201


# FUNCAO PARA REQUISTAR OU CRIAR UMA CATEGORIA PELA ROTA DE CRIAÇÃO DE TRANSAÇÃO
def get_category(category_name):
    category = Category.query.filter(
        Category.name == category_name, Category.user_id == current_user.id
    ).first()

    if category:
        return category.id

    new_category = Category(
        name=category_name.strip().lower(),  # transformando texto em caixa baixa
        user_id=current_user.id,
    )
    db.session.add(new_category)
    db.session.commit()

    return new_category.id


# RETORNA TODAS AS CATEGORIAS DO USUARIO
def get_categories():
    categories = Category.query.filter(Category.user_id == current_user.id).all()

    if not categories:
        return {"message": "Categories not found"}, 404

    all_categories = [
        {
            "category_id": c.id,
            "category_name": c.name,
            "user_id": c.user_id,
        }
        for c in categories
    ]

    return all_categories, 200


def update_category_name(data, category_id):
    category = Category.query.filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()

    new_category_name = data.get("category_name").strip().lower()

    if category:
        # SE CATEGORIA EXISTIR, VERIFICO SE JA EXISTE ALGUMA CATEGORIA COM O MESMO NOME
        if Category.query.filter(
            Category.name == new_category_name, Category.user_id == current_user.id
        ).first():
            return {"message": "Category name already exists"}, 409

        category.name = new_category_name
        db.session.commit()

        return {"message": "Category name updated successfully"}, 200

    return {"message": "Category not found"}, 404


def delete_category_unused(category_id):
    category = Category.query.filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()

    if category:
        category_used = Transaction.query.filter(
            Transaction.category_id == category_id,
            Transaction.user_id == current_user.id,
        ).first()

        if category_used:
            return {
                "message": "Category used in a transaction",
                "transaction": {
                    "id": category_used.id,
                    "description": category_used.description,
                    "date": category_used.date,
                    "amount": category_used.amount,
                    "type": category_used.type,
                    "category": category_used.category.name,
                },
            }, 400

        db.session.delete(category)
        db.session.commit()

        return {"message": "Category deleted successfully"}, 200

    return {"message": "Category not found"}, 404
