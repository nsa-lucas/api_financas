from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Enter your first and last name."),
    )
    email = fields.Email(
        required=True, error_messages={"invalid": "Invalid email format."}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=8, error="The password must contain at least 8 characters."
        ),
    )
    categories = fields.Nested("CategorySchema", many=True, exclude=("user_id",))
    transactions = fields.Nested("TransactionSchema", many=True, exclude=("user_id",))
    created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
# users_schema = UserSchema(many=True)
