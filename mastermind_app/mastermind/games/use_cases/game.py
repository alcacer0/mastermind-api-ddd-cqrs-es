from mastermind.shared.model import UniqueID
from .dto import GameConfigDTO
from ..model import Game, GameWriteRepository, Code


def create_new_game_with_code_to_break(operation_id: UniqueID, game_config: GameConfigDTO, repo: GameWriteRepository) -> Game:
    game = Game.create(game_id=UniqueID(), max_guesses=game_config.max_guesses, operation_id=operation_id)
    game.code_to_break = Code()
    repo.save(game)
    return game
