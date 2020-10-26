from marshmallow import Schema, fields, validate, pre_load

from mastermind.games.model import Code, Game


class GameSchema(Schema):
    game_id = fields.Str(dump_only=True)
    max_guesses = fields.Int(required=True, validate=validate.OneOf(Game.MAX_GUESSES))


class CodeGuessSchema(Schema):
    code = fields.List(fields.Str(validate=validate.OneOf(Code.COLORS)), max=4, min=4)


class FeedbackSchema(Schema):
    blacks = fields.Int(dump_only=True)
    whites = fields.Int(dump_only=True)
