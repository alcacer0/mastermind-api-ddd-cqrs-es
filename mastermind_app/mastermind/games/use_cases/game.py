from mastermind.shared.model import UniqueID
from .dto import GameConfigDTO, CodeGuessDTO
from ..model import Game, GameWriteRepository, Code, Feedback


def create_new_game_with_code_to_break(operation_id: UniqueID, game_config: GameConfigDTO, repo: GameWriteRepository) -> Game:
    game = Game.create(game_id=UniqueID(), max_guesses=game_config.max_guesses, operation_id=operation_id)
    game.code_to_break = Code()
    repo.save(game)
    return game


def make_a_code_guess(operation_id: UniqueID, code_guess: CodeGuessDTO, repo: GameWriteRepository) -> Feedback:
    guess = Code(code_guess.code)
    game = repo.get_by_id(UniqueID(code_guess.game_id))
    game.add_guess(guess=guess, operation_id=operation_id)
    repo.save(game)
    return game.get_feedback(guess)
