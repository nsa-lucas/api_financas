from marshmallow import Schema, fields, validate
from datetime import datetime

from app.models.category import Category


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    type = fields.Str(
        required=True,
        validate=validate.OneOf(["income", "expense"]),
    )
    date = fields.Date(load_default=lambda: datetime.now().date())
    user_id = fields.Str(required=True, load_only=True)
    category_id = fields.Int(required=True, load_only=True)
    category_name = fields.Method("get_category_name", dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    def get_category_name(self, obj):
        category = Category.query.get(obj.category_id)

        return category.name


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
