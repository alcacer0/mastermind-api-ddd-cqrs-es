from marshmallow import Schema, fields, validate, pre_load

from mastermind.games.model import Code, Game


class CodeWithFeedbackSchema(Schema):
    code = fields.List(fields.Str(), attribute='value')
    feedback = fields.Method('get_feedback')

    def get_feedback(self, obj, **kwargs):
        if 'game' not in self.context:
            return None

        game = self.context['game']
        feedback = game.get_feedback(obj)
        return FeedbackSchema().dump(feedback)


class GameSchema(Schema):
    game_id = fields.Str(dump_only=True)
    max_guesses = fields.Int(required=True, validate=validate.OneOf(Game.MAX_GUESSES))
    points = fields.Int(dump_only=True)
    finished = fields.Bool(dump_only=True)
    decoded = fields.Bool(dump_only=True)
    guesses = fields.List(fields.Nested(CodeWithFeedbackSchema), dump_only=True)
    code_to_break = fields.Method('get_code_to_break', dump_only=True)

    def get_code_to_break(self, obj, **kwargs):
        if 'game' not in self.context:
            return None

        game = self.context['game']
        if game.finished:
            return game.code_to_break.value
        return None


class CodeGuessSchema(Schema):
    code = fields.List(fields.Str(validate=validate.OneOf(Code.COLORS)), max=4, min=4)


class FeedbackSchema(Schema):
    blacks = fields.Int(dump_only=True)
    whites = fields.Int(dump_only=True)
