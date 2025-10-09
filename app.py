from flask import Flask

from extensions import db, cors, migrate
from routes import register_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)
register_routes(app)

@app.route('/')
def init_app():
  return 'Hello world'

# Modo debug - DEV
if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
