from flask import request, jsonify, Blueprint
from models.transaction import Transaction
from extensions import db

transactions_bp = Blueprint('transactions',__name__, url_prefix='/api/transactions')

@transactions_bp.route('/add', methods=['POST'])
def add_transactions():
  data = request.json

  if data.get('description') and data.get('value') and data.get('type') and data.get('date'):

    if data['type'] != 'receita' and data['type'] != 'despesa':

      return jsonify({'message': 'Invalid transaction data'}), 400

    transaction = Transaction(
      description = data['description'],
      value = data['value'],
      type = data['type'],
      date = data['date'],
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
      'message': 'Transaction added successfully',
    })
  
  return jsonify({'message': 'Invalid transaction data'}), 400


@transactions_bp.route('/', methods=['GET'])
def transactions():
  transactions = Transaction.query.all()

  all_transactions = []

  if transactions:

    for transaction in transactions:
      all_transactions.append({
        'id': transaction.id,
        'description': transaction.description,
        'value': transaction.value,
        'type': transaction.type,
        'date': transaction.date
      })

    return jsonify(all_transactions)

  return jsonify({'message': 'Transactions not found'})

@transactions_bp.route('/delete/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
  transaction = Transaction.query.get(transaction_id)

  if transaction:
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted successfully'})
    
  return jsonify({'message': 'Transaction not found'}), 404

@transactions_bp.route('/update/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
  data = request.json

  transaction = Transaction.query.get(transaction_id)

  if transaction:
    transaction.description = data.get('description', transaction.description)
    transaction.value = data.get('value', transaction.value)
    transaction.type = data.get('type', transaction.type)
    transaction.date = data.get('date', transaction.date)

    db.session.commit()

    return jsonify({'message': 'Transaction updated successfully'})

  return jsonify({'message': 'Transaction not found'}), 404
