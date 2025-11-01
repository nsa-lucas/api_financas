from marshmallow import Schema, fields, validate


class FilterTransactionsSchema(Schema):
    page = fields.Int(load_default=1)
    limit = fields.Int(load_default=10)
    category_name = fields.Str(load_default="")
    type = fields.Str(
        validate=validate.OneOf(["income", "expense"]),
        error_messages={
            "validator_failed": "The type should be income or expense or nothing'."
        },
    )
    order_by_date = fields.Str(
        load_default="desc",
        validate=validate.OneOf(["desc", "asc"]),
        error_messages={
            "validator_failed": "The order_by_date should be DESC or ASC'."
        },
    )
    order_by_amount = fields.Str(
        load_default="",
        validate=validate.OneOf(["desc", "asc"]),
        error_messages={
            "validator_failed": "The order_by_amount should be DESC or ASC'."
        },
    )


filter_transaction_schema = FilterTransactionsSchema()
