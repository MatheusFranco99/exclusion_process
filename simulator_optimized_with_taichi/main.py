""" Main """

import argparse
import random
import taichi as ti
import matplotlib.pyplot as plt
import numpy as np

from visualization import (ExecutionConfig, visualize_particles_and_metric_combined, visualize_simulation)
from exclusion_process import ExclusionProcessWithMetric

# Plot type
PARTICLES = "particles"
MEASURE = "measure"
ALL = "all"
COMBINED = "combined"

# Initialize Taichi
ti.init(arch=ti.cpu, debug=True)

# Execution argumets
parser = argparse.ArgumentParser(description="Exclusion process visualization.")
parser.add_argument("--n", type=int, required=True, help="Torus size.")
parser.add_argument("--d", type=float, required=True, help="Density of particles (e.g., 0.1 for 10 percent).")
parser.add_argument("--alpha", type=float, required=True, help="Alpha value.")
parser.add_argument("--beta", type=float, required=True, help="Beta value.")
parser.add_argument("--max_p", type=int, required=False, default = 1, help="Maximum particles per site.")
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
    # random.shuffle(particles)
    # particles = 50*[0] + [100]  + [0] * 49

    # Create exclusion process object
    exclusion_process = ExclusionProcessWithMetric(particles = particles, alpha = args.alpha, beta = args.beta, max_particles_per_site = args.max_p)
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

    print(str(ec.exclusion_process.calls_per_site))

    # Convert absolute frequencies to percentages
    count_values = ec.exclusion_process.calls_per_site.to_numpy()
    total = sum(count_values)
    print("Total:", total)
    bins = list(range(len(count_values)))
    percentages = [f / total * 100 for f in count_values]

    # Plot the histogram
    plt.bar(bins, percentages, align='edge', edgecolor='black')

    # # Format the y-axis to show percentage
    # plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

    # Add labels and title
    plt.xlabel('Bins')
    plt.ylabel('Percentage')
    plt.title('Histogram with Percentage Values')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
