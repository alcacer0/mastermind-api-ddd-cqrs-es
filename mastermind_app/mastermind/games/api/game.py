from flask import request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from .operation_id import get_operation_id
from .schema import GameSchema, CodeGuessSchema, FeedbackSchema
from ..use_cases import GameConfigDTO, create_new_game_with_code_to_break,\
    CodeGuessDTO, make_a_code_guess
from ..composition_root import get_game_write_repo

mastermind_games_api = Api()


class GameResource(Resource):
    def post(self):
        try:
            schema = GameSchema()
            args = schema.load(request.get_json())

            operation_id = get_operation_id(args)
            game_config = GameConfigDTO(**args)
            with get_game_write_repo() as game_repo:
                new_game = create_new_game_with_code_to_break(
                    operation_id=operation_id, game_config=game_config, repo=game_repo)
                return schema.dump(new_game), 201

        except ValidationError as err:
            return {"message": err.messages}, 422
        except ValueError as err:
            return {"message": str(err)}, 400


class CodeGuessResource(Resource):
    def post(self, game_id):
        try:
            schema = CodeGuessSchema()
            args = schema.load(request.get_json())

            operation_id = get_operation_id(args)
            guess = CodeGuessDTO(game_id=game_id, **args)
            with get_game_write_repo() as game_repo:
                feedback = make_a_code_guess(
                    operation_id=operation_id, code_guess=guess, repo=game_repo)
                return FeedbackSchema().dump(feedback), 201

        except ValidationError as err:
            return {"message": err.messages}, 422
        except ValueError as err:
            return {"message": str(err)}, 400


mastermind_games_api.add_resource(GameResource, '/games')
mastermind_games_api.add_resource(CodeGuessResource, '/games/<game_id>/guesses')