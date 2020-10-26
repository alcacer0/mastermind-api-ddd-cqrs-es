from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GameConfigDTO:
    max_guesses: int


@dataclass(frozen=True)
class CodeGuessDTO:
    game_id: str
    code: List[str]
