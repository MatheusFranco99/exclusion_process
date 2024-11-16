# Exclusion Process Simulator using Taichi

## Usage

```bash
usage: main.py [-h] --n N --d D --alpha ALPHA --beta BETA --steps STEPS
               {show_particles,show_empirical_measure_complete,show_empirical_measure_speed_up} ...

Exclusion process visualization.

positional arguments:
  {show_particles,show_empirical_measure_complete,show_empirical_measure_speed_up}
    show_particles      Show particles.
    show_empirical_measure_complete
                        Show empirical measure visualization.
    show_empirical_measure_speed_up
                        Show empirical measure visualization with skipped states for speed-up.

options:
  -h, --help            show this help message and exit
  --n N                 Torus size.
  --d D                 Density of particles.
  --alpha ALPHA         Alpha value.
  --beta BETA           Beta value.
  --steps STEPS         Number of steps.
```

For the `show_empirical_measure_speed_up` command, there's an extra argument:
```bash
usage: main.py show_empirical_measure_speed_up [-h] --skipped_steps SKIPPED_STEPS

options:
  -h, --help            show this help message and exit
  --skipped_steps SKIPPED_STEPS
                        Number of steps to skip for speed-up.
```


Examples:

```bash
python3 main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 10000 show_particles
python3 main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 10000 show_empirical_measure_complete
python3 main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 10000 show_empirical_measure_speed_up --skipped_steps 100
```
