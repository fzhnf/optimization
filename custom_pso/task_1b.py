import random
import matplotlib.pyplot as plt


# fungsi objektif yang akan dioptimasi
def obj_func(x: float) -> float:
    return round(((4.0 * x**2) + x - 2.0) ** 2, 4)


class PSO:
    # konstruktor digunakan untuk menginisialisasi nilai awal dari soal
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

    def find_p_best(self) -> None:
        for i, (x, old_x) in enumerate(zip(self.x, self.old_x)):
            self.p_best[i] = x if obj_func(x) < obj_func(old_x) else old_x

    def find_g_best(self) -> None:
        f_values: list[float] = [obj_func(i) for i in self.x]
        minimum_index: int = f_values.index(min(f_values))
        self.g_best = (
            self.x[minimum_index]
            if obj_func(self.x[minimum_index]) < obj_func(self.g_best)
            else self.g_best
        )

    def update_v(self) -> None:
        for i, (v, x, p_best) in enumerate(zip(self.v, self.x, self.p_best)):
            self.v[i] = (
                (self.w * v)
                + (self.c[0] * self.r[0] * (p_best - x))
                + (self.c[1] * self.r[1] * (self.g_best - x))
            )

    def update_x(self) -> None:
        for i, (x, v) in enumerate(zip(self.x, self.v)):
            self.old_x[i], self.x[i] = x, x + v

    def iterate(self, n) -> None:
        print(
            f"""Iterasi ke-0
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
            print(
                f"""iterasi ke-{i+1}
1.) menentukan x = = {[f"{i:.4f}" for i in self.old_x]}
2.) menentukan f(x) = {[f"{obj_func(i):.4f}" for i in self.old_x]}
3.) menentukan gBest = {self.g_best:.4f}
4.) menentukan pBest = {[f"{i:.4f}" for i in self.p_best]}
5.) menentukan v = {[f"{i:.4f}" for i in self.v]}
6.) update x = {[f"{i:.4f}" for i in self.x]}\n"""
            )

        print(f"nilai minimum dari f(x) adalah {obj_func(self.g_best)}")


def main() -> None:
    v_0: float = 0.0
    c_1: float = 0.5
    c_2: float = 1.0
    r_1: float = round(random.random(), 4)
    r_2: float = round(random.random(), 4)
    w: float = 1.0
    particles: list[float] = [float(random.randint(-4, 4)) for _ in range(10)]
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


if __name__ == "__main__":
    main()
