import attr
from typing import List

from mastermind.shared.model.event import BaseEvent


@attr.s(frozen=True)
class GameCreated(BaseEvent):
    game_id: str = attr.ib(kw_only=True)
    max_guesses: int = attr.ib(kw_only=True)


@attr.s(frozen=True)
class GameCodeToBreakDefined(BaseEvent):
    game_id: str = attr.ib(kw_only=True)
    code: List[str] = attr.ib(kw_only=True)
