
cpu_profile:
	python3 -m cProfile -o out.pstats main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 100 show_metric_with_jumps --skipped_steps 1000
	gprof2dot -f pstats out.pstats | dot -Tpng -o image_output.png

show_particles:
	python3 main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 10000 show_particles
show_measure:
	python3 main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 10000 show_empirical_measure_complete
show_measure_speed_up:
	python3 main.py --n 100 --d 0.2 --alpha 2 --beta 0.2 --steps 10000 show_empirical_measure_speed_up --skipped_steps 100
