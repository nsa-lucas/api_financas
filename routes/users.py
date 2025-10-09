from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash

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
  
  

@users_bp.route('/', methods=['GET'])
def users():
  users = User.query.all()

  users_list = []

  for user in users:
    users_list.append({
      "name": user.name,
      "email": user.email,
      "password": user.password
    })
  
  return jsonify(users_list)