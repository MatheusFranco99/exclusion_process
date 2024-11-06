""" Clock """

from dataclasses import dataclass
from datetime import datetime
from typing import Callable
import numpy as np

ClockGenerator = Callable[[], float]

now = datetime.now()
nanoseconds = now.timestamp() * 1_000_000_000
SEED = int(nanoseconds % 1000)
rng = np.random.default_rng(SEED)

def exponential_generator(scale: float) -> ClockGenerator:
    """ Returns a generator for the exponential distribution """
    def generator() -> float:
        global rng
        return rng.exponential(scale=scale, size=1)[0]
    return generator

@dataclass
class Clock:
    """ Clock """
    next_time: float
    generator: ClockGenerator

    def next(self, current_time: float) -> None:
        """ Updates the next sampled time """
        self.next_time = current_time + self.generator()

    def erase(self) -> None:
        """ Erases the timer """
        self.next_time = -1
