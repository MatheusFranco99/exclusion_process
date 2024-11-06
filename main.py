""" Main """

import argparse
from metrics import EmpiricalMeasureMetric, heat_map
from simulator import Simulator, SimulatorConfig, animate_matrics

parser = argparse.ArgumentParser(description="Simple Exclusion Process Simulator with alpha/(n^beta) rate at site 0")
parser.add_argument("-n", type=int, default=100, help="Torus size")
parser.add_argument("-alpha", type=float, default=100.0, help="Alpha parameter for clock rate at site 0")
parser.add_argument("-beta", type=float, default=1.0, help="Beta parameter for clock rate at site 0")
parser.add_argument("-density", type=float, default=0.1, help="Density of particles")
parser.add_argument("-time", type=int, default=10000, help="Stopping time")

def main():
    """ Main """
    args = parser.parse_args()
    config = SimulatorConfig(
        n=args.n,
        alpha=args.alpha,
        beta=args.beta,
        density=args.density,
        max_time=args.time,
    )

    # Run the simulation
    simulator = Simulator(config)
    simulator.setup()
    metrics = simulator.run()

    # Animate the metrics
    animate_matrics(metrics, config)

# TODO
def analyse_several_executions():
    """ Analyses several executions with a heat map animation per time interval"""
    args = parser.parse_args()
    config = SimulatorConfig(
        n=args.n,
        alpha=args.alpha,
        beta=args.beta,
        density=args.density,
        max_time=args.time,
    )
    repetitions = 10
    all_metrics = []
    for _ in range(repetitions):
        simulator = Simulator(config)
        simulator.setup()
        metrics = simulator.run()
        all_metrics.append(metrics)

    heat_map([metric[EmpiricalMeasureMetric] for metric in all_metrics])


if __name__ == "__main__":
    main()
