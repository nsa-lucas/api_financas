import json
from flask import request, jsonify, Blueprint
from flask_login import login_required, logout_user

from services.user_service import create_user, user_login

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/add', methods=['POST'])
def add_user():
  data = request.json

  if data.get('name') and data.get('email') and data.get('password'):
    
    response, status = create_user(data)

    return jsonify(response), status
  
  return jsonify({'message': 'Invalid user data'}), 400

@users_bp.route('/login', methods=['POST'])
def login():
  data = request.json

  response, status = user_login(data)

  return jsonify(response), status

@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  
  return jsonify({'message':'Exiting...'})