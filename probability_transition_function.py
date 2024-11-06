""" Probability transition function """

import random
from typing import Callable
from position import Position

# The transition function. It receives:
# - the particle's position
# - the torus size
# and outputs a new position

ProbabilityTransitionFunction = Callable[[int, int], int] # (Position, N) -> Position

def symmetric_transition() -> ProbabilityTransitionFunction:
    """ Symmetric transition function """

    def rule(position: Position, n: int) -> Position:
        shift = random.choice([-1, 1]) # Randomly chose to go left or right
        new_position = position + shift
        return new_position % n
    return rule
