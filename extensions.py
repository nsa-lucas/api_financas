from flask import jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = "login"
db = SQLAlchemy()
cors = CORS()
migrate = Migrate()


# TRATATIVA CASO TENTE ACESSAR ROTA SEM ESTAR AUTENTICADO
@login_manager.unauthorized_handler
def unauthorized_access():
    return jsonify({"message": "Access denied, authentication required"}), 401
