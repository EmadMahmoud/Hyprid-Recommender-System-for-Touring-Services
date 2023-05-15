from marshmallow import Schema, fields, validate, post_load


class MatchSchema(Schema):
    place_id = fields.Str(load_only=True)
    user_dict = fields.Dict(
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=20)),
        load_only=True
    )
    score = fields.Dict(
        keys=fields.Str(default="similarity"),
        values=fields.Float(validate=validate.Range(min=0, max=5)),
        dump_only=True
    )


class RecommendationsSchema(Schema):
    user_dict = fields.Dict(
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=20)),
        load_only=True
    )
    Recommendations = fields.List(fields.List(fields.Integer), dump_only=True)


class ManualSchema(Schema):
    places_id = fields.List(fields.Integer, load_only=True)
    start_position = fields.List(fields.Float, validate=validate.Length(2), load_only=True)
    num_days = fields.Integer(validate=validate.Range(min=1), load_only=True)
    plan = fields.List(fields.List(fields.Integer), dump_only=True)


class AISchema(Schema):
    user_dict = fields.Dict(
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=20)),
        load_only=True
    )
    city_name = fields.Str(load_only=True)
    start_position = fields.List(fields.Float, validate=validate.Length(2), load_only=True)
    num_days = fields.Integer(validate=validate.Range(min=1), load_only=True)
    plan = fields.List(fields.List(fields.Integer), dump_only=True)


class MakeSquare(Schema):
    place_id = fields.Integer(load_only=True)
    dict_square = fields.Dict(
        Keys=fields.Str(),
        values=fields.Float(),
        dump_only=True
    )


