from flask import request, jsonify, Blueprint
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User
from services.user_service import create_user

users_bp = Blueprint('users', __name__, url_prefix='/api/users')
from flask_migrate import current

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

  user = User.query.filter_by(email = data['email']).first()

  if not user:
    return jsonify({'message':'Email or password invalid'}), 400 

  password_check = check_password_hash(user.password, data['password'])

  if password_check:

    login_user(user)

    return jsonify({'message':'Authorized login'}), 202
  
  return jsonify({'message':'Email or password invalid'}), 400 
  

@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  
  return jsonify({'message':'Exiting...'})