from flask import request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from .operation_id import get_operation_id
from .schema import GameSchema, CodeGuessSchema, FeedbackSchema
from ..use_cases import GameConfigDTO, create_new_game_with_code_to_break,\
    CodeGuessDTO, make_a_code_guess
from ..composition_root import get_game_write_repo
from mastermind.shared.model import AppException, StatusCodes


mastermind_games_api = Api()


class GameListResource(Resource):
    def post(self):
        try:
            schema = GameSchema()
            args = schema.load(request.get_json())

            operation_id = get_operation_id(args)
            game_config = GameConfigDTO(**args)
            with get_game_write_repo() as game_repo:
                new_game = create_new_game_with_code_to_break(
                    operation_id=operation_id, game_config=game_config, repo=game_repo)
                return schema.dump(new_game), StatusCodes.CREATED.value

        except AppException as err:
            return {"message": str(err)}, err.status
        except ValidationError as err:
            return {"message": err.messages}, StatusCodes.INVALID_USER_DATA.value
        except ValueError as err:
            return {"message": str(err)}, StatusCodes.INVALID_REQUEST.value
        except Exception as err:
            # Logging important (connected to Sentry, for example)
            return str(err), StatusCodes.INTERNAL_SERVER_ERROR.value


class GameResource(Resource):
    def get(self, game_id):
        try:
            with get_game_write_repo() as game_repo:
                game = game_repo.get_by_id(aggregate_id=game_id)
                return GameSchema(context={'game': game}).dump(game), StatusCodes.OK.value

        except AppException as err:
            return {"message": str(err)}, err.status
        except ValueError as err:
            return {"message": str(err)}, StatusCodes.INVALID_REQUEST.value
        except Exception as err:
            # Logging important (connected to Sentry, for example)
            return str(err), StatusCodes.INTERNAL_SERVER_ERROR.value


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
                return FeedbackSchema().dump(feedback), StatusCodes.CREATED.value

        except AppException as err:
            return {"message": str(err)}, err.status
        except ValidationError as err:
            return {"message": err.messages}, StatusCodes.INVALID_USER_DATA.value
        except ValueError as err:
            return {"message": str(err)}, StatusCodes.INVALID_REQUEST.value
        except Exception as err:
            return str(err), StatusCodes.INTERNAL_SERVER_ERROR.value


mastermind_games_api.add_resource(GameListResource, '/games')
mastermind_games_api.add_resource(GameResource, '/games/<game_id>')
mastermind_games_api.add_resource(CodeGuessResource, '/games/<game_id>/guesses')