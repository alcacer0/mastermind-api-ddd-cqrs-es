import random

from dataclasses import dataclass, field
from typing import List


COLORS = ['Red', 'Blue', 'Green', 'Yellow']


def random_code() -> List[str]:
    return [random.choice(COLORS) for _ in range(4)]


@dataclass(frozen=True)
class Code:
    value: List[str] = field(default_factory=random_code)

    def __post_init__(self):
        if len(self.value) != 4:
            raise ValueError('A code has 4 pegs')

        for color in self.value:
            if color not in COLORS:
                raise ValueError(f'Color {color} is not supported ({COLORS})')