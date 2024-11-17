
cpu_profile:
	python3 -m cProfile -o out.pstats main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out particles --delay 0 --plot particles
	gprof2dot -f pstats out.pstats | dot -Tpng -o image_output.png

show_particles:
	python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out particles --delay 0 --plot particles
show_measure:
	python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out measure --delay 0 --plot measure
show_combined:
	python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 100 --skipped_steps 0 --out combined --delay 0.1 --plot combined
show_measure_speed_up:
	python3 main.py --n 100 --d 0.1 --alpha 2 --beta 0.2 --steps 1000 --skipped_steps 100 --out measure_speed_up --delay 0 --plot measure
