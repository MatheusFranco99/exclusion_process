# Exclusion Process Simulator using Taichi

## Usage

```bash
usage: main.py [-h] --n N --d D --alpha ALPHA --beta BETA --steps STEPS [--skipped_steps SKIPPED_STEPS] [--out OUT] [--delay DELAY] --plot PLOT

Exclusion process visualization.

options:
  -h, --help            show this help message and exit
  --n N                 Torus size.
  --d D                 Density of particles (e.g., 0.1 for 10 percent).
  --alpha ALPHA         Alpha value.
  --beta BETA           Beta value.
  --steps STEPS         Number of steps.
  --skipped_steps SKIPPED_STEPS
                        Number of steps to skip for speed-up.
  --out OUT             Output directory for video.
  --delay DELAY         Time delay between iterations for better live visualization.
  --plot PLOT           Plot to be done: particles,measure,all,combined.
```


Examples:

```bash
# show particles
python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skippedw teps 0 --out particles --delay 0 --plot particles
# show measure
python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out measure --delay 0 --plot measure
# show both
python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out measure --delay 0 --plot all
# show both combined in one plot
python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out combined --delay 0.1 --plot combined
# show measure speed up
python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 1000 --skipped_steps 100 --out measure_speed_up --delay 0 --plot measure
```
