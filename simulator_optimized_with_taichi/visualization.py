""" Visualizatino functions """

import os
import sys
import time
import taichi as ti

from exclusion_process import ExclusionProcess, ExclusionProcessWithMetric

def visualize_particles(exclusion_process: ExclusionProcess, num_steps: int):
    """ Run simulation and visualize particles """
    gui = ti.GUI("Particle Simulation", (800, 200))

    torus_size = exclusion_process.x.shape[0]

    last_time = 0

    for _ in range(num_steps):

        exclusion_process.process_next_event()

        # Skip if it is printing a previous time due to parallelism
        current_time = exclusion_process.current_time[None]
        if last_time > current_time:
            continue
        last_time = current_time

        # White background
        gui.clear(0xFFFFFF)

        # X axis
        gui.line((0, 0.5), (1, 0.5), radius=2, color=0x222222)

        # Render particles
        for i in range(exclusion_process.size):
            if exclusion_process.x[i] == 1:
                x_coord = i / torus_size
                gui.circle((x_coord, 0.5), radius=10, color=0x3D3BF3)

        # Show current time
        gui.text(content=f"Timestamp: {current_time:.2f}", pos=(0.8, 0.92), color=0x0)

        # Show
        gui.show()


def visualize_empirical_measure(exclusion_process: ExclusionProcessWithMetric, steps: int, state_skip_for_speed_up: int = 0):
    """ Run simulation and visualize empirial measure """
    gui = ti.GUI("Empirial Measure Visualization", (800, 400))

    last_time = 0

    for _ in range(steps):

        exclusion_process.process_next_event()

        # Skip if it is printing a previous time due to parallelism
        current_time = exclusion_process.current_time[None]
        if last_time > current_time:
            continue
        last_time = current_time

        time.sleep(0.1)

        # Compute the metric
        exclusion_process.compute_metric()

        # Draw the metric
        x = exclusion_process.metric_x_points
        y = exclusion_process.metric_values.to_numpy()

        # Scale x and y to GUI coordinates
        x_scaled = (x * 0.8) + 0.1
        y_scaled = (y * 0.8) + 0.1

        # White background
        gui.clear(0xFFFFFF)

        # Axes
        gui.line(begin=(0.1, 0.1), end=(0.9, 0.1), radius=2, color=0x000000)
        gui.line(begin=(0.1, 0.1), end=(0.1, 0.9), radius=2, color=0x000000)

        # Axes labels
        gui.text(content="0", pos=(0.07, 0.07), color=0x000000)
        gui.text(content="1", pos=(0.07, 0.92), color=0x000000)
        gui.text(content="0", pos=(0.1, 0.05), color=0x000000)
        gui.text(content="1", pos=(0.88, 0.05), color=0x000000)

        # Grid
        for i in range(11):
            # Vertical
            x_pos = 0.1 + i * 0.08
            gui.line(begin=(x_pos, 0.1), end=(x_pos, 0.9), radius=1, color=0xDDDDDD)

            # Horizontal
            y_pos = 0.1 + i * 0.08
            gui.line(begin=(0.1, y_pos), end=(0.9, y_pos), radius=1, color=0xDDDDDD)

        # Metric
        for i in range(len(x_scaled) - 1):
            gui.line(begin=(x_scaled[i], y_scaled[i]),
                     end=(x_scaled[i + 1], y_scaled[i + 1]),
                     radius=2,
                     color=0x3D3BF3)  # Orange for the metric line

        # Show current time
        gui.text(content=f"Timestamp: {current_time:.2f}", pos=(0.8, 0.92), color=0x0)

        # Show
        gui.show()

        # Run next event (and skip some states for speed up)
        if state_skip_for_speed_up > 0:
            for _ in range(state_skip_for_speed_up):
                exclusion_process.process_next_event()
