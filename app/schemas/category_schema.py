from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    # Referências
    transactions = fields.Nested("TransactionSchema", many=True, exclude=("category",))
    user_id = fields.Int(required=True)
