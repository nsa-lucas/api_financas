from flask import Flask, jsonify

from extensions import db, cors, login_manager, migrate
from routes import register_routes
from config import Config

application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)
login_manager.init_app(application)
migrate.init_app(application, db)
cors.init_app(application)
register_routes(application)


@application.route("/")
def init_app():
    return jsonify({"status": "ok", "message": "API running", "version": "1.0"})


# Modo debug - DEV
if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run(debug=True)
