from flask import Flask, jsonify

from extensions import db, migrate, cors, jwt
from routes import register_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)
cors.init_app(
    app,
    supports_credentials=True,
    origins=["http://localhost:4200"],
)
register_routes(app)


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API running", "version": "1.0"})


# Modo debug - DEV
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
