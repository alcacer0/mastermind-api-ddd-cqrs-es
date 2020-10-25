from marshmallow import Schema, fields, validate, pre_load


class GameSchema(Schema):
    game_id = fields.Str(dump_only=True)
    max_guesses = fields.Int(required=True, validate=validate.OneOf([12, 10, 8, 6]))
