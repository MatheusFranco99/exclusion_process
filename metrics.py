""" Empirical Measure """

import abc
from dataclasses import dataclass
from typing import Callable

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from system import System

@dataclass
class Metric(abc.ABC):
    """ Metric holds the:
    - metric's name
    - the metric's calculator for given a state
    - a sequence of metric values
    - the associated timestamp for each metric value
    """
    name: str
    getter: callable
    values: list
    timestamps: list[float]

    def add(self, state: System, timestamp: float) -> None:
        """ Adds a new value with a timestamp """
        self.values.append(self.getter(state))
        self.timestamps.append(timestamp)

    def animate(self, torus_size: int) -> None:
        """ Creates an animation through time """

# =========================================
# Empirical Measure
# =========================================

EmpirialMeasure = Callable[[float], float]

def get_empirical_measure(state: System) -> EmpirialMeasure:
    """ Computes the empirical measure """

    # Torus size
    n: int = len(state.positions)

    # Initial empty function
    func: EmpirialMeasure = lambda x: 0

    def add_dirac_mass(func: EmpirialMeasure, point: float) -> EmpirialMeasure:
        # Outputs a new function: func + dirac mass at the given point
        def new_func(x: float) -> float:
            if x >= point:
                return func(x) + 1
            else:
                return func(x)
        return new_func

    # Adds the dirac mass for each point
    for idx, position in enumerate(state.positions):
        if position.particle is not None:
            func = add_dirac_mass(func, idx/n)

    # Normalize by the torus size
    return lambda x: func(x)/n

class EmpiricalMeasureMetric(Metric):
    """ Empirical Measure Metric """

    def __init__(self):
        super().__init__("Empirical Measure",get_empirical_measure,[],[])

    def animate(self, torus_size: int):
        """ Animate the empirical measure through time """

        # Define the x values from 0 to 1
        x = np.linspace(0, 1, 100)

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize = (15,8))
        line, = ax.plot([], [], lw=2, linestyle = "-")

        # Set axis limits
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 0.5)  # Adjust as needed based on function range
        y_max = max([value(1) for value in self.values])
        timestamp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', color='black')

        # Initialization function for FuncAnimation
        def init():
            line.set_data([], [])
            timestamp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', color='black')
            return line, timestamp_text

        # Animation function: updates the line for each frame
        def animate(i):
            y = [self.values[i](xx) for xx in x]
            line.set_data(x, y)
            timestamp_text.set_text(f'Timestamp: {self.timestamps[i]}')
            return line, timestamp_text

        # Create the animation
        anim = FuncAnimation(fig, animate, init_func=init, frames=len(self.values), interval=1)

        plt.grid()
        ax.set_ylim(0, y_max*1.1)
        plt.ylabel("Empirical Measure")
        plt.xlabel("x")
        plt.show()

# =========================================
# Position Profile
# =========================================

def get_position_profile(state: System) -> list[int]:
    """ Returns a list of x indexes where particles are located (from 0 to n-1) """
    ret = []

    for idx, pos in enumerate(state.positions):
        # Add position index if it has a particle
        if pos.particle is not None:
            ret.append(idx)

    return ret

class PositionProfileMetric(Metric):
    """ Position Profile Metric """

    def __init__(self):
        super().__init__("Position Profile", get_position_profile, [], [])

    def animate(self, torus_size: int):
        """ Create an animation of the particle movements on the grid """
        fig, ax = plt.subplots(figsize = (15,8))
        ax.set_xlim(0, torus_size)
        ax.set_ylim(0.49, 0.51)
        ax.set_yticks([])
        ax.set_xticks([i for i in range(torus_size)])
        plt.axhline(y=0.5, color='gray', linestyle='-', linewidth=1)

        scatter = ax.scatter([], [], s=100, color='blue')
        timestamp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', color='black')

        def init1():
            scatter.set_offsets(np.empty((0, 2)))
            timestamp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', color='black')
            return scatter, timestamp_text

        def update1(frame):
            x = self.values[frame]
            y = [0.5] * len(x)
            scatter.set_offsets(np.c_[x, y])
            timestamp_text.set_text(f'Timestamp: {self.timestamps[frame]}')
            return scatter, timestamp_text

        ani = FuncAnimation(fig, update1, frames=len(self.values), init_func=init1, interval=10)
        plt.grid()
        plt.ylabel("Position Profile")
        plt.xlabel("x")
        plt.show()


# TODO
def heat_map(all_metrics: list[EmpiricalMeasureMetric]) -> None:
    """ Animate the empirical measure through time """

    # Define the x values from 0 to 1
    x = np.linspace(0, 1, 100)

    # Set up the figure and axis
    fig, ax = plt.subplots()

    # Set axis limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)  # Adjust as needed based on function range
    y_max = max([value(1) for value in all_metrics[0].values])
    ylim = y_max*1.1
    timestamp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', color='green')

    data: dict[float, list] = {}

    for metric in all_metrics:
        for idx, timestamp in enumerate(metric.timestamps):
            if timestamp not in data:
                data[timestamp] = []
            data[timestamp] += [(xx, metric.values[idx](xx)) for xx in x]
    timestamps = sorted(list(data.keys()))

    # Initialization function for FuncAnimation
    def init():
        ax.clear()
        ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', color='yellow')

    # Animation function: updates the line for each frame
    def animate(i):
        ax.clear()  # Clear the axis to redraw the histogram
        timestamp = timestamps[i]
        x_values = [x[0] for x in data[timestamp]]
        y_values = [x[1] for x in data[timestamp]]
        ax.hist2d(x_values, y_values, bins=30, range=[[0, 1], [0, ylim]], cmap='viridis')
        ax.text(0.05, 0.95, f'Timestamp: {timestamp}', transform=ax.transAxes, ha='left', va='top', color='green')

    # Create the animation
    anim = FuncAnimation(fig, animate, init_func=init, frames=len(timestamps), interval=1)

    plt.grid()
    ax.set_ylim(0, ylim)
    plt.ylabel("Empirical Measure")
    plt.xlabel("x")
    plt.show()
