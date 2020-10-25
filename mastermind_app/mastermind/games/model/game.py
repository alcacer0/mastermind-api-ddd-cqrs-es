from typing import List

from mastermind.shared.model import AggregateRoot, UniqueID, EventStream
from .code import Code
from .events import GameCreated, GameCodeToBreakDefined


class Game(AggregateRoot):
    @staticmethod
    def create(game_id: UniqueID, max_guesses: int, operation_id: UniqueID) -> 'Game':
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

    @AggregateRoot.apply.register
    def _(self, event: GameCodeToBreakDefined) -> None:
        self._code_to_break = Code(event.code)

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

    def __str__(self):
        return f'Game {self.game_id} - max: {self.max_guesses}'
