from marshmallow import Schema, fields, validate, post_load


class MatchSchema(Schema):
    place_id = fields.Integer(load_only=True)
    user_dict = fields.Dict(
        validate=validate.Length(max=20),
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=5)),
        load_only=True
    )
    score = fields.Dict(
        keys=fields.Str(default="similarity"),
        values=fields.Float(validate=validate.Range(min=0, max=5)),
        dump_only=True
    )


class RecommendationsSchema(Schema):
    user_dict = fields.Dict(
        validate=validate.Length(max=20),
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=5)),
        load_only=True
    )
    Recommendations = fields.List(fields.List(fields.Integer), dump_only=True)


class ManualSchema(Schema):
    places_id = fields.List(fields.Integer, load_only=True)
    longitude = fields.Float()
    latitude = fields.Float()
    days = fields.Integer(validate=validate.Range(min=1, max=7), load_only=True)
    plan = fields.List(fields.List(fields.Integer), dump_only=True)


class AISchema(Schema):
    user_dict = fields.Dict(
        validate=validate.Length(max=20),
        keys=fields.Integer(),
        values=fields.Integer(validate=validate.Range(min=0, max=5)),
        load_only=True
    )
    city = fields.Str(load_only=True)
    longitude = fields.Float()
    latitude = fields.Float()
    days = fields.Integer(validate=validate.Range(min=1, max=7), load_only=True)
    plan = fields.List(fields.List(fields.Integer), dump_only=True)


class MakeSquare(Schema):
    place_id = fields.Integer(load_only=True)
    dict_square = fields.Dict(
        Keys=fields.Str(),
        values=fields.Float(),
        dump_only=True
    )


