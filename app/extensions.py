from flask_cors import CORS  # pyright: ignore[reportMissingModuleSource]
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # pyright: ignore[reportMissingModuleSource]

db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()
migrate = Migrate()
blacklist = set()
