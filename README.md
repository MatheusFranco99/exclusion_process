# Exclusion Process Simulator

This repo contains a simulator for the symmetric exclusion process on the discrete torus (0, 1, ..., n-1) with a slight modification that, at site $0$, the clock rate is

$$\frac{\alpha}{n^\beta}$$

rather than $1$ as at other sites.

## Usage

The program runs the simulator and shows two animations: the particle profit and the empirical measure through time.

```bash
usage: main.py [-h] [-n N] [-alpha ALPHA] [-beta BETA] [-density DENSITY]
               [-time TIME]

Simple Exclusion Process Simulator with alpha/(n^beta) rate at site 0

options:
  -h, --help        show this help message and exit
  -n N              Torus size
  -alpha ALPHA      Alpha parameter for clock rate at site 0
  -beta BETA        Beta parameter for clock rate at site 0
  -density DENSITY  Density of particles
  -time TIME        Stopping time
```

Example:

```bash
python3 main.py -n 100 -density 0.2 -alpha 1 -beta 1 -time 100
```

## Code Documentation

- **Particle**: represents a particle with a unique identifier (unused for now).
- **Clock**: an abstract clock that has a generator and keeps track of the next triggered time in the *next_time_* variable.
- **Position**: a position of the system lattice (here a discrete torus), here identifier with an x coordinate of 0 to n-1.
  - The position may have a _particle_ (or not, and in this case it's _None_).
  - The position has also an associated clock used whenever there's a particle at it.
- **ProbabilityTransitionFunction**: the probability transition function receives a certain position, the torus size, and outputs a new position for a particle.
- **TimestampHeap**: a data structure that manages clocks' triggering times. It allows an efficient fetch of the next minimum and update of times.
- **System**: holds a sequence of positions and perform particle movement based on clock events.
- **Simulator**: the simulator receives a configuration (n, alpha, beta, density, and maximum time) and performs the simulation.
  - The _setup_ function creates the initial state.
  - The _run_ function calls the system's *process_next_event* function until the a time limit is reached.
