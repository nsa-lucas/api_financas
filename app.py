from flask import Flask, jsonify

from extensions import db, migrate, cors, jwt
from routes import register_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(
    app,
    resources={r"/api/*": {"origins": "http://localhost:4200"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)
jwt.init_app(app)
register_routes(app)


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API running", "version": "1.0"})


# Modo debug - DEV
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
