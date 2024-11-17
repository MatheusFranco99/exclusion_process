""" Main """

import argparse
import random
import taichi as ti

from visualization import (ExecutionConfig, visualize_particles_and_metric_combined, visualize_simulation)
from exclusion_process import ExclusionProcessWithMetric

# Plot type
PARTICLES = "particles"
MEASURE = "measure"
ALL = "all"
COMBINED = "combined"

# Initialize Taichi
ti.init(arch=ti.cpu)

# Execution argumets
parser = argparse.ArgumentParser(description="Exclusion process visualization.")
parser.add_argument("--n", type=int, required=True, help="Torus size.")
parser.add_argument("--d", type=float, required=True, help="Density of particles (e.g., 0.1 for 10 percent).")
parser.add_argument("--alpha", type=float, required=True, help="Alpha value.")
parser.add_argument("--beta", type=float, required=True, help="Beta value.")
parser.add_argument("--steps", type=int, required=True, help="Number of steps.")
parser.add_argument("--skipped_steps", type=int, default = 0, required=False, help="Number of steps to skip for speed-up.")
parser.add_argument("--out", type=str, required=False, help="Output directory for video.")
parser.add_argument("--delay", type=float, required=False, help="Time delay between iterations for better live visualization.")
parser.add_argument("--plot", type=str, required=True, help=f"Plot to be done: {PARTICLES},{MEASURE},{ALL},{COMBINED}.")


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

    output_dir = "./output/" + args.out

    ec = ExecutionConfig(
        exclusion_process = exclusion_process,
        steps = args.steps,
        state_skip_for_speed_up = args.skipped_steps,
        delay = args.delay,
        output_dir=output_dir)

    if args.plot == COMBINED:
        visualize_particles_and_metric_combined(ec)
    elif args.plot == PARTICLES:
        visualize_simulation(ec, show_particles = True, show_measure = False)
    elif args.plot == MEASURE:
        visualize_simulation(ec, show_particles = False, show_measure = True)
    elif args.plot == ALL:
        visualize_simulation(ec, show_particles = True, show_measure = True)

if __name__ == "__main__":
    main()
