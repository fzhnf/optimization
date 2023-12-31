import matplotlib.pyplot as plt


def obj_func(x: float) -> float:
    return round(((4.0 * x**2) + x - 2.0) ** 2, 4)


class PSO:
    def __init__(
        self,
        x: list[float],
        v: list[float],
        c: list[float],
        r: list[float],
        w: float,
    ) -> None:
        self.x: list[float] = x
        self.v: list[float] = v
        self.c: list[float] = c
        self.r: list[float] = r
        self.w: float = w

        self.old_x: list[float] = x.copy()
        self.p_best: list[float] = x.copy()
        f_values: list[float] = [obj_func(i) for i in x.copy()]
        self.g_best: float = x[f_values.index(min(f_values))]

        self.x_history: list[list[float]] = []
        self.p_best_history: list[list[float]] = []
        self.g_best_history: list[float] = []
        self.v_history: list[list[float]] = []
        self.f_x_history: list[float] = []

    def find_p_best(self) -> None:
        print(
            "self.p_best[i] = x[i] if obj_func(x[i]) < obj_func(old_x[i]) else old_x[i]"
        )
        for i, (x, old_x) in enumerate(zip(self.x, self.old_x)):
            self.p_best[i] = x if obj_func(x) < obj_func(old_x) else old_x
            print(
                f"self.p_best[{i}] = {x} if {obj_func(x)} < {obj_func(old_x)} else {old_x}"
            )
        print(f"self.p_best = {self.p_best}\n")

    def find_g_best(self) -> None:
        print(
            "self.g_best = self.x[min_idx] if obj_func(self.x[min_idx]) < obj_func(self.g_best) else self.g_best"
        )
        f_values: list[float] = [obj_func(i) for i in self.x]
        min_idx: int = f_values.index(min(f_values))
        self.g_best = (
            self.x[min_idx]
            if obj_func(self.x[min_idx]) < obj_func(self.g_best)
            else self.g_best
        )
        print(
            f"self.g_best = {self.x[min_idx]} if {obj_func(self.x[min_idx])} < {obj_func(self.g_best)} else {self.g_best}\n"
        )
        print(f"self.g_best = {self.g_best} {min_idx}\n")

    def update_v(self) -> None:
        print(
            "self.v[i] = (self.w * v[i]) + (self.c[0] * self.r[0] * (p_best[i] - x[i])) + (self.c[1] * self.r[1] * (self.g_best - x[i]))"
        )
        for i, (v, x, p_best) in enumerate(zip(self.v, self.x, self.p_best)):
            self.v[i] = (
                (self.w * v)
                + (self.c[0] * self.r[0] * (p_best - x))
                + (self.c[1] * self.r[1] * (self.g_best - x))
            )
            print(
                f"self.v[{i}] = ({self.w} * {v}) + ({self.c[0]} * {self.r[0]} * ({p_best} - {x})) + ({self.c[1]} * {self.r[1]} * ({self.g_best} - {x}))"
            )
            print(f"self.v[{i}] = {self.v[i]}\n")

    def update_x(self) -> None:
        print("self.old_x[i], self.x[i] = x[i], x[i] + v[i]")
        for i, (x, v) in enumerate(zip(self.x, self.v)):
            self.old_x[i], self.x[i] = x, x + v
            print(f"self.old_x[{i}], self.x[{i}] = {x}, {x} + {v}")
            print(f"self.old_x[{i}], self.x[{i}] = {self.old_x[i]}, {self.x[i]}\n")

    def iterate(self, n) -> None:
        print(
            f"""Iterasi ke-0
fungsi objektif = (4x^2 + x - 2)^2
nilai x = {self.x}
nilai v = {self.v}
nilai c = {self.c}
nilai r = {self.r}
nilai w = {self.w}
"""
        )
        for i in range(n):
            self.find_g_best()
            self.find_p_best()
            self.update_v()
            self.update_x()

            self.x_history.append(self.old_x.copy())
            self.p_best_history.append(self.p_best.copy())
            self.g_best_history.append(self.g_best)
            self.v_history.append(self.v.copy())
            self.f_x_history.append(obj_func(self.g_best))

        #             print(
        #                 f"""iterasi ke-{i+1}
        # 1.) menentukan x = {self.old_x}
        # 2.) menentukan f(x) = {[obj_func(i) for i in self.old_x]}
        # 3.) menentukan gBest = {self.g_best}
        # 4.) menentukan pBest = {self.p_best}
        # 5.) menentukan v = {self.v}
        # 6.) update x = {self.x}\n"""
        #             )

        print(f"nilai minimum dari f(x) adalah {obj_func(self.g_best)}")

    def plot(self):
        fig, axs = plt.subplots(2, 2, figsize=(15, 15))

        axs[0, 0].plot(range(1, len(self.x_history) + 1), self.x_history)
        axs[0, 0].legend(["x_0", "x_1", "x_2"])
        axs[0, 0].set_xlabel("iterasi")
        axs[0, 0].set_ylabel("nilai x")
        axs[0, 0].set_title("x")

        axs[0, 1].plot(range(1, len(self.p_best_history) + 1), self.p_best_history)
        axs[0, 1].legend(["p_best_0", "p_best_1", "p_best_2"])
        axs[0, 1].set_xlabel("iterasi")
        axs[0, 1].set_ylabel("nilai p_best")
        axs[0, 1].set_title("p_best")

        axs[1, 0].plot(range(1, len(self.g_best_history) + 1), self.g_best_history)
        axs[1, 0].set_xlabel("iterasi")
        axs[1, 0].set_ylabel("nilai g_best")
        axs[1, 0].set_title("g_best")

        axs[1, 1].plot(range(1, len(self.v_history) + 1), self.v_history)
        axs[1, 1].legend(["v_0", "v_1", "v_2"])
        axs[1, 1].set_xlabel("iterasi")
        axs[1, 1].set_ylabel("nilai v")
        axs[1, 1].set_title("v")

        plt.tight_layout(h_pad=6)
        plt.show()

        fig, ax = plt.subplots(
            figsize=(5, 5)
        )  # Create a new figure with a single subplot

        ax.plot(range(1, len(self.f_x_history) + 1), self.f_x_history)
        ax.set_xlabel("iterasi")
        ax.set_ylabel("nilai f(x)")
        ax.set_title("f(x)")

        plt.tight_layout()
        plt.show()


def main() -> None:
    x_0: float = 0.0
    x_1: float = 0.5
    x_2: float = 1.0
    v_0: float = 0.0
    c_1: float = 0.5
    c_2: float = 1.0
    r_1: float = 0.5
    r_2: float = 0.5
    w: float = 1.0
    particles: list[float] = [x_0, x_1, x_2]
    velocities: list[float] = [v_0 for _ in range(len(particles))]
    acceleration_coefficients: list[float] = [c_1, c_2]
    random_numbers: list[float] = [r_1, r_2]
    inertia_weight: float = w
    pso: PSO = PSO(
        particles,
        velocities,
        acceleration_coefficients,
        random_numbers,
        inertia_weight,
    )
    pso.iterate(3)
    # pso.plot()


if __name__ == "__main__":
    main()
