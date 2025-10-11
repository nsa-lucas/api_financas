from flask_login import current_user

from extensions import db
from models.Category import Category


def create_category(category_name):
    category = Category(
        name=category_name.strip().lower(),  # transformando texto em caixa baixa
        user_id=current_user.id,
    )
    db.session.add(category)
    db.session.commit()

    return int(category.id)


def get_category(category_name):
    category = Category.query.filter(
        Category.name == category_name, Category.user_id == current_user.id
    ).first()

    if not category:
        category = create_category(category_name)

    return int(category.id)
