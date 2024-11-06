""" System """

from dataclasses import dataclass
import random
import numpy as np
from position import Position
from probability_transition_function import ProbabilityTransitionFunction
from timestamp_heap import TimestampHeap

@dataclass
class System:
    """ The system is characterized by:
    - n: the torus' size
    - positions: a list of positions [0, 1, ..., n-1] which can hold a particle or be empty
    - transition_function: a transition function that accepts (a position, the torus size) and returns a new position
    - event_queue: a queue with clock expiry events
    - current_time: the current time
    """
    n: int
    positions: list[Position]
    transition_function: ProbabilityTransitionFunction
    event_queue: TimestampHeap
    current_time: float

    def __init__(self, n: int, positions: list[Position], transition_function: ProbabilityTransitionFunction):
        self.n = n
        self.positions = positions
        self.transition_function = transition_function
        self.event_queue = TimestampHeap()
        self.current_time = 0

        # Fill up the queue
        for idx, position in enumerate(self.positions):
            if position.particle is None:
                position.clock.erase()
            else:
                position.clock.next(0)
                next_time = position.clock.next_time
                self.event_queue.add_or_update(idx, next_time)

    def is_empty(self, position: int) -> bool:
        """ Returns whether a position is empty or not """
        return self.positions[position].particle is None

    def restart_clock(self, position: int, current_time: float) -> None:
        """ Restarts the clock of a given position """
        self.positions[position].clock.next(current_time)

    def erase_clock(self, position: int) -> None:
        """ Erases the clock of a given position """
        self.positions[position].clock.erase()

    def get_next_trigger_time(self, position: int) -> float:
        """ Get the triggering time of the clock of a given position """
        return self.positions[position].clock.next_time

    def move(self, position: int, new_position: int) -> None:
        """ Moves a particle to a new position.
        It assumes the new position is empty
        """
        if not self.is_empty(new_position):
            raise AssertionError("Position is occupied")
        if self.is_empty(position):
            raise AssertionError("No particle is position")

        # Update state
        self.positions[new_position].particle = self.positions[position].particle
        self.positions[position].particle = None

    def clock_triggered(self, position: int, current_time: float) -> None:
        """ Implements the trigerring of a clock and try to move a particle """
        # Get new position for particle
        new_position = self.transition_function(position, self.n)

        # Check if site occupied
        if not self.is_empty(new_position):
            # If so, restart the clock
            self.restart_clock(position, current_time)
            self.event_queue.add_or_update(position, self.get_next_trigger_time(position))
        else:
            # If empty, move particle and restart clock at new position
            self.move(position, new_position)

            self.restart_clock(new_position, current_time)
            self.event_queue.add_or_update(new_position, self.get_next_trigger_time(new_position))

            self.erase_clock(position)
            self.event_queue.remove_key(position)

    def process_next_event(self) -> None:
        """ Processes the next event """
        result = self.event_queue.pop_min()
        if result is None:
            raise AssertionError("No more events in the queue")

        position = result[0]
        self.current_time = result[1]
        self.clock_triggered(position, self.current_time)

def create_initial_state(n, density=0.5) -> np.ndarray[int]:
    """ Creates an initial state """

    # state = np.random.choice([0, 1], size=n, p=[1 - density, density])

    occupied_spaces = int(density * n)
    state = [1] * occupied_spaces + [0] * (n - occupied_spaces)
    random.shuffle(state)
    return state
