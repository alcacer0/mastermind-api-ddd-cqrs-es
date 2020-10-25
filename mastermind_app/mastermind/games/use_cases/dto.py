from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfigDTO:
    max_guesses: int
