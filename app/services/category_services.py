from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction


def create_category(category_name):
    current_user = get_jwt_identity()

    category_name = category_name.strip().lower()

    category = Category.query.filter(
        Category.name == category_name, Category.user_id == current_user
    ).first()

    if category:
        return category.id

    category = Category(
        name=category_name,
        user_id=current_user,
    )
    db.session.add(category)
    db.session.commit()

    return category.id


def get_categories():
    current_user = get_jwt_identity()

    categories = Category.query.filter(Category.user_id == current_user).all()

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
    current_user = get_jwt_identity()

    category = Category.query.filter(
        Category.id == category_id, Category.user_id == current_user
    ).first()

    new_category_name = data.get("category_name").strip().lower()

    if category:
        if Category.query.filter(
            Category.name == new_category_name, Category.user_id == current_user
        ).first():
            return {"message": "Category name already exists"}, 409

        category.name = new_category_name
        db.session.commit()

        return {"message": "Category name updated successfully"}, 200

    return {"message": "Category not found"}, 404


def delete_category_unused(category_id):
    current_user = get_jwt_identity()

    category = Category.query.filter(
        Category.id == category_id, Category.user_id == current_user
    ).first()

    if category:
        category_used = Transaction.query.filter(
            Transaction.category_id == category_id,
            Transaction.user_id == current_user,
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
