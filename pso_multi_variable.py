def obj_func(x: float, y: float) -> float:
    return 0.26 * (x**2 + y**2) - 0.48 * x * y


class PSO:
    def __init__(
        self,
        x: list[float],
        y: list[float],
        v: list[float],
        c: list[float],
        r: list[float],
        w: float,
    ) -> None:
        self.x: list[float] = x
        self.y: list[float] = y
        self.v: list[list[float]] = [[x, y] for x, y in zip(v, v)]
        self.c: list[float] = c
        self.r: list[float] = r
        self.w: float = w

        self.old_x: list[float] = x.copy()
        self.old_y: list[float] = y.copy()
        self.p_best: list[list[float]] = [[x, y] for x, y in zip(x, y)]

        fvalues = [obj_func(x, y) for x, y in zip(self.x, self.y)]
        self.g_best: list[float] = [
            self.x[fvalues.index(min(fvalues))],
            self.y[fvalues.index(min(fvalues))],
        ]

    def find_p_best(self) -> None:
        for i, (x, y, old_x, old_y) in enumerate(
            zip(self.x, self.y, self.old_x, self.old_y)
        ):
            self.p_best[i] = (
                [x, y]
                if obj_func(x, y) < obj_func(old_x, old_y)
                else [
                    old_x,
                    old_y,
                ]
            )

    def find_g_best(self) -> None:
        fValues = [obj_func(x, y) for x, y in zip(self.x, self.y)]
        minimumIndex = fValues.index(min(fValues))
        self.g_best = (
            [self.x[minimumIndex], self.y[minimumIndex]]
            if obj_func(self.x[minimumIndex], self.y[minimumIndex])
            < obj_func(self.g_best[0], self.g_best[1])
            else self.g_best
        )

    def update_velocities(self) -> None:
        for i, (x, y) in enumerate(zip(self.x, self.y)):
            self.v[i][0] = (
                (self.w * self.v[i][0])
                + (self.c[0] * self.r[0] * (self.p_best[i][0] - x))
                + (self.c[1] * self.r[1] * (self.g_best[0] - x))
            )
            self.v[i][1] = (
                (self.w * self.v[i][1])
                + (self.c[0] * self.r[0] * (self.p_best[i][1] - y))
                + (self.c[1] * self.r[1] * (self.g_best[1] - y))
            )

    def update_particles(self) -> None:
        for i, (x, y) in enumerate(zip(self.x, self.y)):
            self.old_x[i], self.old_y[i] = x, y
            self.x[i], self.y[i] = x + self.v[i][0], y + self.v[i][1]

    def iterate(self, n) -> None:
        print(
            f"""Iterasi ke-0
nilai (x,y) = {list(zip(self.x, self.y))}
nilai (vx,vy) = {self.v}
nilai c = {self.c}
nilai r = {self.r}
nilai w = {self.w}
"""
        )
        for i in range(n):
            self.find_p_best()
            self.find_g_best()
            self.update_velocities()
            self.update_particles()
            print(
                f"""Iterasi ke-{i+1}
1.) menentukan (x,y) = {list(zip(self.old_x, self.old_y))}
2.) menentukan f(x,y) = {[round(obj_func(x, y),4) for x, y in zip(self.old_x, self.old_y)]}
3.) menentukan gBest = {self.g_best}
4.) menentukan pBest = {self.p_best}
5.) menentukan (vx,vy) = {self.v}
6.) update (x,y) = {list(zip(self.x, self.y))}\n"""
            )
        print(
            f"Nilai minimum dari f(x,y) adalah {obj_func(self.g_best[0], self.g_best[1]):.4f}"
        )


x_0, y_0 = 1.0, 1.0
x_1, y_1 = -2.0, -1.0
x_2, y_2 = 2.0, 2.0
v_0 = 0.0
c_1 = 1.0
c_2 = 0.5
r_1 = 1.0
r_2 = 1.0
w = 1.0

particles_x, particles_y = [x_0, x_1, x_2], [y_0, y_1, y_2]
velocities = [v_0 for _ in range(len(particles_x))]
acceleration_coefficients = [c_1, c_2]
random_numbers = [r_1, r_2]
inertia_weight = w
pso = PSO(
    particles_x,
    particles_y,
    velocities,
    acceleration_coefficients,
    random_numbers,
    inertia_weight,
)
pso.iterate(3)
