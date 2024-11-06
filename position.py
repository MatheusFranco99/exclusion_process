""" Position """

from dataclasses import dataclass
from clock import Clock
from particle import Particle

@dataclass
class Position:
    """ Position represents a site at the torus. It has the:
        - x coordinate
        - a clock associated to the position
        - a particle (if there's any)
    """
    x: int
    clock: Clock
    particle: Particle | None
