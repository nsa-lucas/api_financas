from .transactions import transactions_bp
from .users import users_bp
from .categories import categories_bp


def register_routes(app):
    app.register_blueprint(transactions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
