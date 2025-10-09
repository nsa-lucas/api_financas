from flask import request, jsonify, Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/add', methods=['GET'])
def add_user():
  return jsonify({
    'message': 'hello users',
  })