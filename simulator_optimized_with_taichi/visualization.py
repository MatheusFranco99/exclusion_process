""" Visualizatino functions """

from dataclasses import dataclass
import os
import sys
import time
import taichi as ti

from exclusion_process import ExclusionProcess, ExclusionProcessWithMetric

@dataclass
class ExecutionConfig:
    """ Configuration for execution """
    exclusion_process: ExclusionProcessWithMetric
    steps: int
    state_skip_for_speed_up: int
    delay: float
    output_dir: str

def init_gui(name: str, size: tuple, output_dir: str):
    """ Init GUI """
    gui = ti.GUI(name, size)
    video_manager = ti.tools.VideoManager(output_dir=output_dir, framerate=24, automatic_build=False)
    return gui, video_manager

def add_particles(gui, ep: ExclusionProcess, torus_size: int, x_0: float, x_scale: float, y: float):
    # Render particles
    for i in range(ep.size):
        if ep.x[i] == 1:
            x_coord = (i / torus_size) * x_scale + x_0
            gui.circle((x_coord, y), radius=10, color=0x3D3BF3)

def add_x_axis(gui, x0, x1, y):
    gui.line((x0, y), (x1, y), radius=2, color=0x222222)

def add_y_axis(gui, x, y0, y1):
    gui.line((x, y0), (x, y1), radius=2, color=0x222222)

def add_time(gui, time: float, pos: tuple):
    gui.text(content=f"Timestamp: {time:.2f}", pos=pos, color=0x0)

def add_chart_labels(gui, x0, x1, y0, y1):
    gui.text(content="0", pos=(x0, y0), color=0x000000)
    gui.text(content="1", pos=(x0, y1), color=0x000000)
    gui.text(content="1", pos=(x1, y0), color=0x000000)

def add_grid(gui, x0, x1, y0, y1):
    # Grid
    for i in range(11):
        # Vertical
        x_pos = x0 + i * (x1-x0)/10
        gui.line(begin=(x_pos, y0), end=(x_pos, y1), radius=1, color=0xDDDDDD)

        # Horizontal
        y_pos = y0 + i * (y1-y0)/10
        gui.line(begin=(x0, y_pos), end=(x1, y_pos), radius=1, color=0xDDDDDD)

def add_metric(gui, x, y):
    for i in range(len(x) - 1):
        gui.line(begin=(x[i], y[i]),
                    end=(x[i + 1], y[i + 1]),
                    radius=2,
                    color=0x3D3BF3)

def skip_states_for_speed_up(exclusion_process, state_skip_for_speed_up):
    if state_skip_for_speed_up > 0:
        for _ in range(state_skip_for_speed_up):
            exclusion_process.process_next_event()
    return exclusion_process

def visualize_simulation(execution_config: ExecutionConfig, show_particles: bool, show_measure: bool):
    """ Run simulation and visualize particles and metric """

    # Unpack config
    exclusion_process: ExclusionProcessWithMetric = execution_config.exclusion_process
    steps: int = execution_config.steps
    state_skip_for_speed_up: int = execution_config.state_skip_for_speed_up
    delay: float = execution_config.delay
    output_dir: str = execution_config.output_dir

    torus_size = exclusion_process.x.shape[0]
    last_time = 0

    # Create GUIs
    particle_gui, particle_video_manager = None, None
    metric_gui, metric_video_manager = None, None
    if show_particles:
        particle_gui, particle_video_manager = init_gui("Particle Simulation", (800, 200), output_dir=os.path.join(output_dir, "particle"))
    if show_measure:
        metric_gui, metric_video_manager = init_gui("Metric Visualization", (800, 400), output_dir=os.path.join(output_dir, "metric"))

    for _ in range(steps):
        exclusion_process.process_next_event()

        current_time = exclusion_process.current_time[None]
        assert last_time <= current_time
        last_time = current_time

        # -------------------
        # Render particles GUI
        # -------------------
        if show_particles:
            particle_gui.clear(0xFFFFFF)
            add_x_axis(particle_gui, 0, 1, 0.5)
            add_particles(particle_gui, exclusion_process, torus_size, 0, 1, 0.5)
            add_time(particle_gui, current_time, (0.8, 0.92))
            particle_video_manager.write_frame(particle_gui.get_image())
            particle_gui.show()

        # -------------------
        # Render metric GUI
        # -------------------
        if show_measure:
            metric_gui.clear(0xFFFFFF)
            add_x_axis(metric_gui, 0.1, 0.9, 0.1)
            add_y_axis(metric_gui, 0.1, 0.1, 0.9)
            add_chart_labels(metric_gui, 0.07, 0.9, 0.05, 0.92)
            add_grid(metric_gui, 0.1, 0.9, 0.1, 0.9)

            exclusion_process.compute_metric()
            x = exclusion_process.metric_x_points
            y = exclusion_process.metric_values.to_numpy()
            x_scaled = (x * 0.8) + 0.1
            y_scaled = (y * 0.8) + 0.1
            add_metric(metric_gui, x_scaled, y_scaled)

            add_time(metric_gui, current_time, (0.8, 0.92))

            metric_video_manager.write_frame(metric_gui.get_image())
            metric_gui.show()

        # Skip states for speed up
        exclusion_process = skip_states_for_speed_up(exclusion_process, state_skip_for_speed_up)

        # Delay for better live visualization
        if delay > 0:
            time.sleep(delay)

    # Finalize videos
    if show_particles:
        particle_video_manager.make_video(gif=True, mp4=True)
    if show_measure:
        metric_video_manager.make_video(gif=True, mp4=True)


def visualize_particles_and_metric_combined(execution_config: ExecutionConfig):
    """ Run simulation and visualize particles and metric in a single GUI """

    # Unpack config
    exclusion_process: ExclusionProcessWithMetric = execution_config.exclusion_process
    steps: int = execution_config.steps
    state_skip_for_speed_up: int = execution_config.state_skip_for_speed_up
    delay: float = execution_config.delay
    output_dir: str = execution_config.output_dir

    torus_size = exclusion_process.x.shape[0]
    last_time = 0

    gui, video_manager = init_gui("Particles and Metric Visualization", (800, 600), output_dir)

    for _ in range(steps):
        exclusion_process.process_next_event()

        current_time = exclusion_process.current_time[None]
        assert last_time <= current_time
        last_time = current_time

        # -------------------
        # Compute metric
        # -------------------
        exclusion_process.compute_metric()
        x = exclusion_process.metric_x_points
        y = exclusion_process.metric_values.to_numpy()

        # Scale metric to GUI coordinates (top half)
        x_scaled = (x * 0.8) + 0.1
        y_scaled = (y * 0.4) + 0.5

        gui.clear(0xFFFFFF)
        add_x_axis(gui, 0.1, 0.9, 0.5)
        add_y_axis(gui, 0.1, 0.5, 0.9)
        add_grid(gui, 0.1, 0.9, 0.5, 0.9)
        add_chart_labels(gui, 0.07, 0.9, 0.47, 0.9)
        add_metric(gui, x_scaled, y_scaled)

        add_x_axis(gui, 0.1, 0.9, 0.25)
        add_particles(gui, exclusion_process, torus_size, 0.1, 0.8, 0.25)

        add_time(gui, current_time, (0.8, 0.92))

        # Save to video
        video_manager.write_frame(gui.get_image())
        gui.show()

        skip_states_for_speed_up(exclusion_process, state_skip_for_speed_up)

        time.sleep(delay)

    # Finalize video
    video_manager.make_video(gif=True, mp4=True)