from flask import request, jsonify, Blueprint
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/add', methods=['POST'])
def add_user():
  data = request.json

  if data.get('name') and data.get('email') and data.get('password'):

    # VERIFICANDO SE EMAIL JA EXISTE
    email_already_exists = User.query.filter_by(email=data['email']).first()

    if email_already_exists:  
      return jsonify({'message':'Email already exists'}), 400

    # CRIPTOGRAFANDO SENHA
    hashed_password = generate_password_hash(data['password'])

    user = User(
      name = data['name'],
      email = data['email'],
      password = hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'})

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

    return jsonify({'message':'Authorized login'})
  
  return jsonify({'message':'Email or password invalid'}), 400 
  

@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()

  return jsonify({'message':'Exiting...'})