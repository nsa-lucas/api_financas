from .transactions_routes import transactions_bp
from .users_routes import users_bp
from .categories_routes import categories_bp


def register_routes(app):
    app.register_blueprint(transactions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
