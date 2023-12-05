# Import library yang dibutuhkan
import random
import matplotlib.pyplot as plt


# fungsi objektif yang akan dioptimasi
def obj_func(x: float, y: float) -> float:
    """
    Menghitung nilai dari fungsi objektif.

    Parameter:
    - x: Variabel pertama
    - y: Variabel kedua

    Kembalian:
    - Nilai yang dihitung dari fungsi objektif
    """
    return 0.39 * (x**2 + y**2) - 0.56 * x * y


# Particle Swarm Optimization (PSO) class
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
        """
        Inisialisasi algoritma PSO dengan posisi partikel, velocities,
        koefisien percepatan, bilangan acak, dan inertia weight.

        Parameter:
        - x: Daftar posisi x
        - y: Daftar posisi y
        - v: Daftar kecepatan partikel
        - c: Daftar koefisien percepatan [c1, c2]
        - r: Daftar bilangan acak [r1, r2]
        - w: Inertia weight
        """
        # Inisialisasi posisi, velocities, koefisien percepatan, bilangan acak, dan inertia weight
        self.x: list[float] = x
        self.y: list[float] = y
        self.v: list[list[float]] = [[x, y] for x, y in zip(v, v)]
        self.c: list[float] = c
        self.r: list[float] = r
        self.w: float = w

        # Inisialisasi posisi terbaik untuk setiap partikel,, dan posisi sebelumnya
        self.old_x: list[float] = x.copy()
        self.old_y: list[float] = y.copy()
        self.p_best: list[list[float]] = [[x, y] for x, y in zip(x, y)]

        # Inisialisasi posisi terbaik global
        f_values = [obj_func(x, y) for x, y in zip(self.x, self.y)]
        self.g_best: list[float] = [
            self.x[f_values.index(min(f_values))],
            self.y[f_values.index(min(f_values))],
        ]

        self.x_history: list[list[float]] = []
        self.y_history: list[list[float]] = []
        self.g_best_x_history: list[float] = []
        self.g_best_y_history: list[float] = []
        self.p_best_x_history: list[list[float]] = []
        self.p_best_y_history: list[list[float]] = []
        self.vx_history: list[list[float]] = []
        self.vy_history: list[list[float]] = []
        self.f_x_history: list[float] = []

    def find_p_best(self) -> None:
        # Memperbarui posisi terbaik untuk setiap partikel
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
        # Memperbarui posisi terbaik diantara semua partikel
        f_values = [obj_func(x, y) for x, y in zip(self.x, self.y)]
        minimum_index = f_values.index(min(f_values))
        self.g_best = (
            [self.x[minimum_index], self.y[minimum_index]]
            if obj_func(self.x[minimum_index], self.y[minimum_index])
            < obj_func(self.g_best[0], self.g_best[1])
            else self.g_best
        )

    def update_velocities(self) -> None:
        """
        Memperbarui kecepatan partikel menggunakan rumus PSO, yaitu:
        vx_i = w * vx_i + c1 * r1 * (pBest_i - x_i) + c2 * r2 * (gBest - x_i)
        vy_i = w * vy_i + c1 * r1 * (pBest_i - y_i) + c2 * r2 * (gBest - y_i)
        """
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
        # Memperbarui posisi partikel berdasarkan velocities yang telah diperbarui
        for i, (x, y) in enumerate(zip(self.x, self.y)):
            self.old_x[i], self.old_y[i] = x, y
            self.x[i], self.y[i] = x + self.v[i][0], y + self.v[i][1]

    def iterate(self, n) -> None:
        # Menjalan algoritma PSO selama n iterasi
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
            self.x_history.append(self.x.copy())
            self.y_history.append(self.y.copy())
            self.g_best_x_history.append(self.g_best[0])
            self.g_best_y_history.append(self.g_best[1])
            self.p_best_x_history.append([x[0] for x in self.p_best])
            self.p_best_y_history.append([y[1] for y in self.p_best])
            self.vx_history.append([vx[0] for vx in self.v])
            self.vy_history.append([vy[1] for vy in self.v])
            self.f_x_history.append(obj_func(self.g_best[0], self.g_best[1]))
            print(
                f"""Iterasi ke-{i+1}
1.) menentukan (x,y) = {[f"({x:.4f}, {y:.4f})" for x, y in zip(self.old_x, self.old_y)]}
2.) menentukan f(x,y) = {[round(obj_func(x, y),4) for x, y in zip(self.old_x, self.old_y)]}
3.) menentukan gBest = {f"({self.g_best[0]:.4f}, {self.g_best[1]:.4f})"}
4.) menentukan pBest = {[f"({x:.4f}, {y:.4f})" for x, y in zip(self.p_best[0], self.p_best[1])]}
5.) menentukan (vx,vy) = {[f"({x:.4f}, {y:.4f})" for x, y in zip(self.v[0], self.v[1])]}
6.) update (x,y) = {[f"({x:.4f}, {y:.4f})" for x,y in zip(self.x, self.y)]}\n"""
            )
        print(
            f"Nilai minimum dari f(x,y) adalah {obj_func(self.g_best[0], self.g_best[1]):.4f}"
        )

    def plot(self) -> None:
        fig, axs = plt.subplots(2, 4, figsize=(15, 10))
        axs[0, 0].plot(range(1, len(self.x_history) + 1), self.x_history)
        axs[0, 0].set_xlabel("iterasi")
        axs[0, 0].set_ylabel("x")
        axs[0, 0].set_title("x")
        axs[0, 1].plot(range(1, len(self.y_history) + 1), self.y_history)
        axs[0, 1].set_xlabel("iterasi")
        axs[0, 1].set_ylabel("y")
        axs[0, 1].set_title("y")
        axs[0, 2].plot(range(1, len(self.g_best_x_history) + 1), self.g_best_x_history)
        axs[0, 2].set_xlabel("iterasi")
        axs[0, 2].set_ylabel("gBest_x")
        axs[0, 2].set_title("gBest_x")
        axs[0, 3].plot(range(1, len(self.g_best_y_history) + 1), self.g_best_y_history)
        axs[0, 3].set_xlabel("iterasi")
        axs[0, 3].set_ylabel("gBest_y")
        axs[0, 3].set_title("gBest_y")
        axs[1, 0].plot(range(1, len(self.p_best_x_history) + 1), self.p_best_x_history)
        axs[1, 0].set_xlabel("iterasi")
        axs[1, 0].set_ylabel("pBest_x")
        axs[1, 0].set_title("pBest_x")
        axs[1, 1].plot(range(1, len(self.p_best_y_history) + 1), self.p_best_y_history)
        axs[1, 1].set_xlabel("iterasi")
        axs[1, 1].set_ylabel("pBest_y")
        axs[1, 1].set_title("pBest_y")
        axs[1, 2].plot(range(1, len(self.vx_history) + 1), self.vx_history)
        axs[1, 2].set_xlabel("iterasi")
        axs[1, 2].set_ylabel("vx")
        axs[1, 2].set_title("vx")
        axs[1, 3].plot(range(1, len(self.vy_history) + 1), self.vy_history)
        axs[1, 3].set_xlabel("iterasi")
        axs[1, 3].set_ylabel("vy")
        axs[1, 3].set_title("vy")
        plt.tight_layout(h_pad=5)
        plt.show()

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(range(1, len(self.f_x_history) + 1), self.f_x_history)
        ax.set_xlabel("iterasi")
        ax.set_ylabel("f(x,y)")
        ax.set_title("f(x,y)")
        plt.show()


# Menyiapkan kondisi awal dan parameter
v_0 = 0.0
c_1 = 1.0
c_2 = 0.5
r_1 = round(random.random(), 4)
r_2 = round(random.random(), 4)
w = 1.0
# nilai (x,y) = [(-4.0, -3.0), (7.0, -1.0), (-7.0, -3.0), (0.0, 4.0), (4.0, 1.0), (-3.0, -5.0), (2.0, -1.0), (-4.0, -2.0), (-8.0, -7.0), (6.0, 0.0)]

x = [-4.0, 7.0, -7.0, 0.0, 4.0, -3.0, 2.0, -4.0, -8.0, 6.0]
y = [-3.0, -1.0, -3.0, 4.0, 1.0, -5.0, -1.0, -2.0, -7.0, 0.0]

# nilai r = [0.2569, 0.7896]
r = [0.2569, 0.7896]
if __name__ == "__main__":
    # Menghasilkan posisi awal secara acak untuk partikel
    # particles_x, particles_y = [float(random.randint(-10, 10)) for _ in range(10)], [
    #     float(random.randint(-10, 10)) for _ in range(10)
    # ]
    particles_x, particles_y = x, y
    velocities = [v_0 for _ in range(len(particles_x))]
    acceleration_coefficients = [c_1, c_2]
    # random_numbers = [r_1, r_2]
    random_numbers = r
    inertia_weight = w

    # Inisialisasi algoritma PSO dan menjalankannya selama 3 iterasi
    pso = PSO(
        particles_x,
        particles_y,
        velocities,
        acceleration_coefficients,
        random_numbers,
        inertia_weight,
    )
    pso.iterate(3)
    pso.plot()
