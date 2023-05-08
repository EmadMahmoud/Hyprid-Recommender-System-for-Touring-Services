from marshmallow import Schema, fields, validate, post_load
from marshmallow.validate import Length, Range


class MatchSchema(Schema):
    place_id = fields.Integer(load_only=True, validate=Range(min=0))
    user_dict = fields.Dict(
        keys=fields.Integer(),
        values=fields.Decimal(validate=validate.Range(min=0, max=5)),
        load_only=True
    )
    score = fields.Decimal(dump_only=True, validate=validate.Range(min=0, max=5))

