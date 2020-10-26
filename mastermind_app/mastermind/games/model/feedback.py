from dataclasses import dataclass


@dataclass(frozen=True)
class Feedback:
    blacks: int
    whites: int

    def __post_init__(self):
        if self.blacks + self.whites > 4 or self.blacks < 0 or self.whites < 0:
            return ValueError('Invalid feedback')
