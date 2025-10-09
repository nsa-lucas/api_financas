from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = 'login'  
db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
