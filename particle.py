""" Particle """


from dataclasses import dataclass

@dataclass
class Particle:
    """ Represents a particle in the system with a certain ID """
    id: int # Unused for now. But feature is added in case we want to track the position of a specific particle
