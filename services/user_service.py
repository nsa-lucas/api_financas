from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User

def create_user(data):

  email = data['email'].strip().lower()

    # VERIFICANDO SE EMAIL JA EXISTE
  if User.query.filter_by(email=email).first():

    return {'message':'Email already exists'}, 409

  # CRIPTOGRAFANDO SENHA
  hashed_password = generate_password_hash(data['password'])

  user = User(
    name = data['name'],
    email = email,
    password = hashed_password
  )

  db.session.add(user)
  db.session.commit()

  return {'message': 'User added successfully'}, 201

