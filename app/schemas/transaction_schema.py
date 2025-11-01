from marshmallow import Schema, fields, validate


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    type = fields.Str(
        required=True,
        validate=validate.OneOf(["income", "expense"]),
        error_messages={"validator_failed": "The type should be income or expense'."},
    )
    date = fields.Date(required=True)
    user_id = fields.Str(required=True)
    category_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
