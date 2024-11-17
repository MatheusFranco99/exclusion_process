""" ExclusionProcess implementation """
import numpy as np
import taichi as ti


@ti.data_oriented
class ExclusionProcess:
    """ Exclusion process """

    def __init__(self, particles: list[int], alpha: float, beta: float):
        self.size = len(particles)
        self.alpha = alpha
        self.beta = beta

        # Initialize the binary field `x` with 1 (occupied site) or 0 (empty)
        self.x = ti.field(ti.i32, shape=self.size)
        for i, has_particle in enumerate(particles):
            self.x[i] = has_particle

        # Initialize a list of clocks for each position
        self.clocks = ti.field(ti.f32, shape=self.size)

        # Initialize current time variable
        self.current_time = ti.field(ti.f32, shape=())
        self.current_time[None] = 0.0  # Start with current_time = 0.0

        # Compute only once the parameter for the exponential distribution at site 0
        self.exp_parameter_at_0 = ti.field(ti.f32, shape=())
        self.exp_parameter_at_0[None] = self.alpha / (self.size ** self.beta)

        # !Deprecated for using taichi random numbers
        # # Get Random Number Generator
        # now = datetime.now()
        # curr_nanoseconds = now.timestamp() * 1_000_000_000
        # seed_for_rng = int(curr_nanoseconds % 1000)
        # self.rng = np.random.default_rng(seed_for_rng)

    @ti.kernel
    def setup(self):
        """ Setups the clocks' values: -1 if site is empty, else an exponential random value"""
        for i in self.x:
            if self.x[i]:
                self.clocks[i] = self.current_time[None] + self.get_exponential(i)
            else:
                self.clocks[i] = -1

    @ti.func
    def get_exponential(self, position: int):
        """ Returns an exponential random value according to the position
        (the position is relevant due to the different exponential parameters at different sites)
        Generation is performed by converting an uniform random value to an exponential one
        """
        ans = 0.0
        if position == 0:
            ans = -1/(self.exp_parameter_at_0[None]) * ti.log(ti.random(ti.f32))
        else:
            ans = -1 * ti.log(ti.random(float))
        return ans

    @ti.kernel
    def print_values(self):
        """ Auxiliary method for describing the state"""
        for i in range(self.x.shape[0]):
            print(f"Index {i}: Particle={self.x[i]}, Value={self.clocks[i]}")

    @ti.kernel
    def process_next_event(self):
        """ Process the next clock event, jumps the particle if possible, and updates the clocks """

        # Find position with minimum clock value (ignoring -1 values)
        min_value = float('inf')
        selected_pos = -1
        for i in range(self.clocks.shape[0]):
            if self.clocks[i] != -1 and self.clocks[i] < min_value:
                min_value = self.clocks[i]
                selected_pos = i

        # Sanity checks
        assert selected_pos != -1 # Should find a value
        assert self.x[selected_pos] == 1 # Should have a particle at the selected site

        # Update current time
        assert self.current_time[None] <= min_value
        self.current_time[None] = min_value

        # Determine random jump direction (left or right) and destination
        direction = ti.random()
        new_pos = -1
        if direction < 0.5:  # Jump left
            new_pos = (selected_pos - 1) % self.x.shape[0]
        else:  # Jump right
            new_pos = (selected_pos + 1) % self.x.shape[0]

        # Only move the particle if the destination is empty
        if self.x[new_pos] == 0:
            # Move the particle
            self.x[selected_pos] = 0
            self.x[new_pos] = 1

            # Update clocks
            self.clocks[selected_pos] = -1
            self.clocks[new_pos] = self.current_time[None] + self.get_exponential(position=new_pos)
        else:
            # If couldn't jump, restarts the clock at the selected position
            self.clocks[selected_pos] = self.current_time[None] + self.get_exponential(position=selected_pos)

@ti.data_oriented
class ExclusionProcessWithMetric(ExclusionProcess):
    """ Exclusion Process with metrics """
    def __init__(self, particles: list[int], alpha: float, beta: float, num_metric_points: int):
        super().__init__(particles, alpha, beta)
        self.metric_values = ti.field(ti.f32, shape=(num_metric_points,))  # Discretized t in [0, 1]
        self.metric_x_points = np.linspace(0, 1, num_metric_points)  # Corresponding t values

    @ti.kernel
    def compute_metric(self):
        """Compute the metric for all metric x points"""
        n = self.size
        for k in range(self.metric_values.shape[0]):
            x_point = k / self.metric_values.shape[0]
            total = 0.0
            for i in range(n):
                if self.x[i] == 1 and x_point >= (i / n):  # Particle at position i contributes with 1 if x >= i/n
                    total += 1.0
            self.metric_values[k] = total / n  # Normalize by dividing by n
