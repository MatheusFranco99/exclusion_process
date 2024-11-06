""" Simulator """

from dataclasses import dataclass
import math

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from system import System, create_initial_state
from position import Position
from clock import Clock, exponential_generator
from particle import Particle
from probability_transition_function import symmetric_transition
from metrics import (EmpiricalMeasureMetric, Metric, PositionProfileMetric)

@dataclass
class SimulatorConfig:
    """ Configuration for the simulator """
    n: int # torus size
    alpha: float
    beta: float
    density: float
    max_time: float

class Simulator:
    """ Simulator """

    def __init__(self, config: SimulatorConfig):
        self.config: SimulatorConfig = config
        self.system: System | None = None
        self.metrics: dict[callable, Metric]| None = None

    def setup(self):
        """ Setups the simulator by:
        - creating an initial state
        - creating the positions 0, ..., n-1
        - initializing the metrics
        """

        # Create initial state
        state = create_initial_state(self.config.n, self.config.density)

        # Create positions 0, ..., n-1
        positions: list[Position] = []
        for i in range(self.config.n):
            # Add particle if any
            particle = None
            if state[i] == 1:
                particle = Particle(i)

            # Set clock rate according to position
            rate = 1
            if i == 0:
                rate = self.config.alpha/pow(self.config.n, self.config.beta)

            # Add position
            position = Position(i, Clock(0, exponential_generator(rate)), particle)
            positions.append(position)

        self.system = System(self.config.n, positions, symmetric_transition())

        # Init metrics
        self.metrics: dict[callable, Metric] = {
            EmpiricalMeasureMetric: EmpiricalMeasureMetric(),
            PositionProfileMetric: PositionProfileMetric(),
        }

    def update_metrics(self, state: System) -> None:
        """ Updates each metric according to new state """
        for metric in self.metrics.values():
            metric.add(state, state.current_time)

    def add_repeted_metrics(self, t1: float, t2: float, delta_t: float) -> None:
        """ The new update is only on metric t2.
        So, from t1 to t2 (with delta_t), we copy the state on
        t1 + delta, t1 + 2*delta, ...
        until t2
        we use the timestamps of the form D.DD
        """
        def next_d_dd(a):
            # Takes the minimum number of form D.DD which is greater than a
            x = math.ceil(a * 100) / 100
            if x == a:
                x += delta_t
            return x
        t = next_d_dd(t1)
        while t < t2:
            # Create repeted metric values
            for metric in self.metrics.values():
                metric.values.append(metric.values[-1])
                metric.timestamps.append(t)
            # Update time
            t += delta_t

    def run(self) -> None:
        """ Runs the simulation until the stopping time """

        current_time = self.system.current_time
        time_step = 0.01

        self.update_metrics(self.system)

        while current_time < self.config.max_time:
            self.system.process_next_event()
            new_time = self.system.current_time
            self.add_repeted_metrics(current_time, new_time, time_step)
            current_time = new_time
            self.update_metrics(self.system)

        return self.metrics

def animate_matrics(metrics: dict[callable,Metric], config: SimulatorConfig) -> None:
    """ Runs metrics animation """
    metrics[PositionProfileMetric].animate(config.n)
    metrics[EmpiricalMeasureMetric].animate(config.n)
