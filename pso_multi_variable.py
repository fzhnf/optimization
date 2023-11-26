import numpy as np
from numpy.typing import NDArray
from typing import Any


def obj_func(x: NDArray, y: NDArray) -> Any:
    return 1 / 3 * np.sqrt(x**2 + y**2 + 25)


class PSO:
    def __init__(
        self, x: NDArray, y: NDArray, v: NDArray, c: NDArray, r: NDArray, w: float
    ) -> None:
        self.x: NDArray = x
        self.y: NDArray = y
        self.velocities_x: NDArray = v
        self.velocities_y: NDArray = v.copy()
        self.coefficients: NDArray = c
        self.ranges: NDArray = r
        self.weight: float = w

        self.old_x: NDArray = x.copy()
        self.old_y: NDArray = y.copy()
        self.p_best_x: Any = x.copy()
        self.p_best_y: Any = y.copy()
        self.g_best_x: Any = self.x[
            np.argmin([obj_func(x, y) for x, y in zip(self.x, self.y)])
        ]
        self.g_best_y: Any = self.y[
            np.argmin([obj_func(x, y) for x, y in zip(self.x, self.y)])
        ]

    def update_personal_best(self) -> None:
        for i in range(len(self.x)):
            value = obj_func(self.x[i], self.y[i])
            p_best_f_value = obj_func(self.p_best_x[i], self.p_best_y[i])
            if value < p_best_f_value:
                self.p_best_x[i] = self.x[i]
                self.p_best_y[i] = self.y[i]
            else:
                self.p_best_x[i] = self.old_x[i]
                self.p_best_y[i] = self.old_y[i]

    def update_global_best(self) -> None:
        minimumIndex = np.argmin([obj_func(x, y) for x, y in zip(self.x, self.y)])
        self.g_best_x = self.x[minimumIndex]
        self.g_best_y = self.y[minimumIndex]

    def update_velocities(self) -> None:
        for i in range(len(self.x)):
            self.velocities_x[i] = (
                (self.weight * self.velocities_x[i])
                + (
                    self.coefficients[0]
                    * self.ranges[0]
                    * (self.p_best_x[i] - self.x[i])
                )
                + (self.coefficients[1] * self.ranges[1] * (self.g_best_x - self.x[i]))
            )
            self.velocities_y[i] = (
                (self.weight * self.velocities_y[i])
                + (
                    self.coefficients[0]
                    * self.ranges[0]
                    * (self.p_best_y[i] - self.y[i])
                )
                + (self.coefficients[1] * self.ranges[1] * (self.g_best_y - self.y[i]))
            )

    def update_positions(self):
        for i in range(len(self.x)):
            self.old_x[i] = self.x[i]
            self.old_y[i] = self.y[i]
            self.x[i] = self.x[i] + self.velocities_x[i]
            self.y[i] = self.y[i] + self.velocities_y[i]

    def iterate(self, n):
        # print(f"Iterasi 0")
        # print(f"x = {self.x}")
        # print(f"y = {self.y}")
        # print(f"vx = {self.velocities_x}")
        # print(f"vy = {self.velocities_y}")
        # print(f"pBest = {self.p_best_x}")
        # print(f"gBest = {self.g_best_x}")
        # print(f"pBest = {self.p_best_y}")
        # print(f"gBest = {self.g_best_y}")
        # print(f"f(gBest x, gBest y) = {f(self.g_best_x, self.g_best_y)}")
        # print()
        print(
            f"""Iterasi 0
Positions x = {self.x}
Positions y = {self.y}
Velocities x = {self.velocities_x}
Velocities y = {self.velocities_y}
Personal best x = {self.p_best_x}
Personal best y = {self.p_best_y}
Global best x = {self.g_best_x}
Global best y = {self.g_best_y}
Objective function value = {obj_func(self.g_best_x, self.g_best_y)}
"""
        )
        for i in range(n):
            self.update_personal_best()
            self.update_global_best()
            self.update_velocities()
            self.update_positions()
            # print(f"Iterasi", i + 1)
            # print(f"x = {self.x}")
            # print(f"y = {self.y}")
            # print(f"vx = {self.velocities_x}")
            # print(f"vy = {self.velocities_y}")
            # print(f"pBest = {self.p_best_x}")
            # print(f"gBest = {self.g_best_x}")
            # print(f"pBest = {self.p_best_y}")
            # print(f"gBest = {self.g_best_y}")
            # print(f"f(gBest x, gBest y) = {obj_func(self.g_best_x, self.g_best_y)}")
            # print(f"f(x, y) = {[obj_func(x, y) for x, y in zip(self.x, self.y)]}")
            # print()
            print(
                f"""Iterasi {i+1}
Positions x = {self.x}
Positions y = {self.y}
Velocities x = {self.velocities_x}
Velocities y = {self.velocities_y}
Personal best x = {self.p_best_x}
Personal best y = {self.p_best_y}
Global best x = {self.g_best_x}
Global best y = {self.g_best_y}
Objective function (Global best) = {obj_func(self.g_best_x, self.g_best_y)}
Objective function (Positions) = {[obj_func(x, y) for x, y in zip(self.x, self.y)]}
"""
            )


# def main():
#     x = np.array([1.0, 1.0, 0.0])
#     y = np.array([1.0, -1.0, 0.0])
#     v = np.array([0.0, 0.0, 0.0])
#     c = np.array([1.0, 1.0])
#     r = np.array([1.0, 0.5])
#     w = 1
#
#     pso = PSO(x, y, v, c, r, w)
#     pso.iterate(1500)
#
#
# if __name__ == "__main__":
#     main()
