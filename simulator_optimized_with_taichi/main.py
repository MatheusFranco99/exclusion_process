""" Main """

import argparse
import random
import taichi as ti

from visualization import visualize_empirical_measure, visualize_particles
from exclusion_process import ExclusionProcessWithMetric

# Initialize Taichi
ti.init(arch=ti.gpu)

# Execution argumets
parser = argparse.ArgumentParser(description="Exclusion process visualization.")
parser.add_argument("--n", type=int, required=True, help="Torus size.")
parser.add_argument("--d", type=float, required=True, help="Density of particles.")
parser.add_argument("--alpha", type=float, required=True, help="Alpha value.")
parser.add_argument("--beta", type=float, required=True, help="Beta value.")
parser.add_argument("--steps", type=int, required=True, help="Number of steps.")
subparsers = parser.add_subparsers(dest="command", required=True)

# Subcommand: show particles
show_particles_parser = subparsers.add_parser("show_particles", help="Show particles.")

# Subcommand: show complete metric
show_empirical_measure_complete = subparsers.add_parser("show_empirical_measure_complete", help="Show empirical measure visualization.")

# Subcommand: show metric with jumps
show_empirical_measure_speed_up = subparsers.add_parser("show_empirical_measure_speed_up", help="Show empirical measure visualization with skipped states for speed-up.")
show_empirical_measure_speed_up.add_argument("--skipped_steps", type=int, required=True, help="Number of steps to skip for speed-up.")



def show_particles(exclusion_process: ExclusionProcessWithMetric, steps: int):
    """ Run particle visualization """
    visualize_particles(exclusion_process, num_steps = steps)

def show_complete_metric(exclusion_process: ExclusionProcessWithMetric, steps: int):
    """ Run particle visualization """
    visualize_empirical_measure(exclusion_process, steps=steps, state_skip_for_speed_up = 0)

def show_metric_with_jumps(exclusion_process: ExclusionProcessWithMetric, steps: int, state_skip: int):
    """ Run particle visualization """
    visualize_empirical_measure(exclusion_process, steps=steps, state_skip_for_speed_up = state_skip)


def main():
    """ Main function """

    # Parse arguments
    args = parser.parse_args()

    # Create particles list
    num_particles = int(args.n * args.d)
    particles = [1] * num_particles + [0] * (args.n - num_particles)
    random.shuffle(particles)

    # Create exclusion process object
    exclusion_process = ExclusionProcessWithMetric(particles = particles, alpha = args.alpha, beta = args.beta, num_metric_points = args.n * 2)
    exclusion_process.setup()

    # Execute appropriate command
    if args.command == "show_particles":
        show_particles(exclusion_process, args.steps)
    elif args.command == "show_empirical_measure_complete":
        show_complete_metric(exclusion_process, args.steps)
    elif args.command == "show_empirical_measure_speed_up":
        show_metric_with_jumps(exclusion_process, args.steps, args.skipped_steps)

if __name__ == "__main__":
    main()
