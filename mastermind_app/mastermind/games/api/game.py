from flask import request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from .operation_id import get_operation_id
from .schema import GameSchema
from ..use_cases import GameConfigDTO, create_new_game_with_code_to_break
from ..composition_root import get_game_write_repo

mastermind_games_api = Api()


class GameResource(Resource):
    def post(self):
        schema = GameSchema()
        try:
            args = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 422

        operation_id = get_operation_id(args)
        game_config = GameConfigDTO(**args)
        print(game_config)
        with get_game_write_repo() as game_repo:
            new_game = create_new_game_with_code_to_break(
                operation_id=operation_id, game_config=game_config, repo=game_repo)
            return schema.dump(new_game), 201


mastermind_games_api.add_resource(GameResource, '/games')
