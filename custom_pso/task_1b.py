import numpy as np
from numpy.typing import NDArray
from typing import Any


def obj_func(x: NDArray) -> Any:
    return (x) / ((x**2) + 1)


class PSO:
    def __init__(
        self,
        x: NDArray,
        v: NDArray,
        c: NDArray,
        r: NDArray,
        w: float,
    ) -> None:
        self.x: NDArray = x
        self.v: NDArray = v
        self.c: NDArray = c
        self.r: NDArray = r
        self.w: float = w

        self.old_x: NDArray = np.copy(x)
        self.p_best: Any = np.copy(x)
        self.g_best: Any = self.x[0]

    def update_personal_best(self) -> None:
        for i in range(len(self.x)):
            self.p_best[i] = (
                self.x[i]
                if obj_func(self.x[i]) < obj_func(self.p_best[i])
                else self.old_x[i]
            )

    def update_global_best(self) -> None:
        x = self.x[np.argmin([obj_func(x) for x in self.x])]
        self.g_best = x if x < self.g_best else self.g_best

    def update_velocities(self) -> None:
        for i in range(len(self.x)):
            self.v[i] = (
                (self.w * self.v[i])
                + (self.c[0] * self.r[0] * (self.p_best[i] - self.x[i]))
                + (self.c[1] * self.r[1] * (self.g_best - self.x[i]))
            )

    def update_positions(self) -> None:
        for i in range(len(self.x)):
            self.old_x[i] = self.x[i]
            self.x[i] = self.x[i] + self.v[i]

    def iterate(self, n) -> None:
        self.update_personal_best()
        self.update_global_best()
        print(
            f"""Iteration 0
Positions = {self.x}
Velocities = {self.v}

"""
        )
        for i in range(n):
            self.update_global_best()
            self.update_personal_best()
            self.update_velocities()

            print(
                f"""Iteration {i + 1}
Positions = {self.x}
Objective function Personal Best = {[obj_func(self.p_best)]}
Objective function Global Best = {[obj_func(self.g_best)]}
Global Best = {self.g_best}
Personal Best = {self.p_best}
Velocities = {self.v}"""
            )
            self.update_positions()
            print(f"Updated Positions = {self.x}\n")


def main():
    x_0 = 0.0
    x_1 = -3.0
    x_2 = -4.0
    v_0 = 0.0
    v_1 = 0.0
    v_2 = 0.0
    c_1 = 0.5
    c_2 = 1.0
    r_1 = r_2 = 0.5
    w = 1.0

    initial_positions = np.array([x_0, x_1, x_2])
    initial_velocities = np.array([v_0, v_1, v_2])
    coefficients = np.array([c_1, c_2])
    ranges = np.array([r_1, r_2])
    weight = w

    pso = PSO(initial_positions, initial_velocities, coefficients, ranges, weight)
    pso.iterate(3)


if __name__ == "__main__":
    main()
