import numpy as np
from numpy.typing import NDArray
from typing import Any


def obj_func(x: NDArray) -> Any:
    return 1 / 3 * np.sqrt(x**2 + 25)


class PSO:
    def __init__(
        self,
        x: NDArray,
        velocities: NDArray,
        coefficients: NDArray,
        ranges: NDArray,
        weight: float,
    ) -> None:
        self.x: NDArray = x
        self.velocities: NDArray = velocities
        self.coefficients: NDArray = coefficients
        self.ranges: NDArray = ranges
        self.weight: float = weight

        self.old_x: NDArray = x.copy()
        self.p_best: Any = x.copy()
        self.g_best: Any = None

    def update_personal_best(self) -> None:
        self.p_best = [
            x if obj_func(x) < obj_func(p_best) else old_x
            for x, p_best, old_x in zip(self.x, self.p_best, self.old_x)
        ]

    def update_global_best(self) -> None:
        self.g_best = self.x[np.argmin([obj_func(x) for x in self.x])]

    def update_velocities(self) -> None:
        for i in range(len(self.x)):
            self.velocities[i] = (
                (self.weight * self.velocities[i])
                + (self.coefficients[0] * self.ranges[0] * (self.p_best[i] - self.x[i]))
                + (self.coefficients[1] * self.ranges[1] * (self.g_best - self.x[i]))
            )

    def update_positions(self) -> None:
        for i in range(len(self.x)):
            self.old_x[i] = self.x[i]
            self.x[i] = self.x[i] + self.velocities[i]

    def iterate(self, n) -> None:
        print(
            f"""Iteration 0
Positions = {self.x}
Velocities = {self.velocities}
"""
        )

        for i in range(n):
            self.update_personal_best()
            self.update_global_best()
            self.update_velocities()
            self.update_positions()
            print(
                f"""Iteration {i + 1}
Positions = {self.x}
Velocities = {self.velocities}
Personal Best = {self.p_best}
Global Best = {self.g_best}
Objective Function (Global Best) = {obj_func(self.g_best)}
Objective Function (Positions) = {[obj_func(x) for x in self.x]}
"""
            )


initial_positions = np.array([-1.0, 1.5, 2.0])
initial_velocities = np.array([0.0, 0.0, 0.0])
coefficients = np.array([0.5, 1])
ranges = np.array([0.5, 0.5])
weight = 1.0

pso = PSO(initial_positions, initial_velocities, coefficients, ranges, weight)
pso.iterate(3)
