from typing import List

from mastermind.shared.model import AggregateRoot, UniqueID, EventStream
from .code import Code
from .feedback import Feedback
from .events import GameCreated, GameCodeToBreakDefined, CodeGuessMade


class Game(AggregateRoot):
    MAX_GUESSES = [12, 10, 8, 6]

    @staticmethod
    def create(game_id: UniqueID, max_guesses: int, operation_id: UniqueID) -> 'Game':
        if max_guesses not in Game.MAX_GUESSES:
            raise ValueError(f'Allowed max guesses values are: {Game.MAX_GUESSES}')

        created_event = GameCreated(
            game_id=game_id.value,
            max_guesses=max_guesses,
            operation_id=operation_id.value
        )
        game = Game(EventStream([created_event]))
        game._initialize([created_event])
        return game

    @AggregateRoot.apply.register
    def _(self, event: GameCreated) -> None:
        self._game_id: UniqueID = UniqueID(event.game_id)
        self._max_guesses: int = event.max_guesses
        self._guesses: List[Code] = []
        self._code_to_break = None
        self._decoded = False

    @AggregateRoot.apply.register
    def _(self, event: GameCodeToBreakDefined) -> None:
        self._code_to_break = Code(event.code)

    @AggregateRoot.apply.register
    def _(self, event: CodeGuessMade) -> None:
        guess = Code(event.code)
        self._guesses.append(guess)
        self._decoded = self.get_feedback(guess).blacks == 4

    @property
    def game_id(self) -> UniqueID:
        return self._game_id

    @property
    def max_guesses(self) -> int:
        return self._max_guesses

    @property
    def guesses(self) -> List[Code]:
        return self._guesses

    @property
    def points(self) -> int:
        points = len(self._guesses)
        if self.finished and not self.decoded:
            points += 1
        return points

    @property
    def decoded(self) -> bool:
        return self._decoded

    @property
    def finished(self) -> bool:
        return self.decoded or len(self.guesses) == self.max_guesses

    @property
    def code_to_break(self) -> Code:
        return self._code_to_break

    @code_to_break.setter
    def code_to_break(self, code: Code):
        if self.code_to_break is not None:
            raise ValueError('This game has already a code to break')
        if len(self.guesses) > 0:
            raise ValueError('This game has one or more guesses')

        self.apply_event(GameCodeToBreakDefined(
            game_id=self.game_id.value,
            code=code.value,
            operation_id=UniqueID().value
        ))

    def add_guess(self, guess: Code, operation_id: UniqueID):
        if self.finished:
            raise ValueError('Can not add a guess to a finished game')

        self.apply_event(CodeGuessMade(
            game_id=self.game_id.value,
            code=guess.value,
            operation_id=operation_id.value
        ))

    def get_feedback(self, guess: Code) -> Feedback:
        """
        Returns a code feedback about the game code. Based on the algorithm
        described in https://en.wikipedia.org/wiki/Mastermind_(board_game)
        """
        whites = blacks = 0
        game_colors = self.code_to_break.value
        guess_colors = guess.value
        for game_c, guess_c in zip(game_colors, guess_colors):
            if game_c == guess_c:
                blacks += 1
            elif guess_c in game_colors:
                guess_c_count = guess_colors.count(guess_c)
                if guess_c_count > 1:
                    if guess_c_count == game_colors.count(guess_c):
                        whites += 1
                else:
                    whites += 1

        return Feedback(blacks=blacks, whites=whites)

    def __str__(self):
        return f'Game {self.game_id} - max-guesses: {self.max_guesses} - ' \
               f'n-guesses: {len(self._guesses)} - decoded: {self.decoded}'
