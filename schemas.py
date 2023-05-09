from marshmallow import Schema, fields, validate, post_load
from marshmallow.validate import Length, Range


class MatchSchema(Schema):
    place_id = fields.Str(load_only=True)
    user_dict = fields.Dict(
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=5)),
        load_only=True
    )
    score = fields.Dict(
        keys=fields.Str(default="similarity"),
        values=fields.Float(validate=validate.Range(min=0, max=5)),
        dump_only=True
    )
