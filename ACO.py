import matplotlib.pyplot as plt
import math
import random

# Konstanta untuk parameter ACO
NUM_ANTS = 20                   # Jumlah semut
MAX_ITERATIONS = 100            # Jumlah iterasi
ALPHA = 1.0                    # Parameter pentingnya feromon
BETA = 1.0                     # Parameter pentingnya visibilitas
RHO = 0.15                     # Tingkat evaporasi feromon
INITIAL_PHEROMONE = 1.0        # Feromon awal pada tiap jalur

class ACO:
    def __init__(self, distances, city_names):
        self.num_cities = len(distances)          # Jumlah kota
        self.distances = distances               # Matriks jarak antar kota
        self.pheromones = [[INITIAL_PHEROMONE for _ in range(self.num_cities)] for _ in range(self.num_cities)]
        self.city_names = city_names             # Nama kota

    def select_next_city(self, current_city, visited):
        probabilities = [0.0] * self.num_cities
        total = 0.0

        # Hitung probabilitas untuk kota yang belum dikunjungi
        for city in range(self.num_cities):
            if not visited[city]:
                pheromone = self.pheromones[current_city][city] ** ALPHA
                visibility = (1.0 / self.distances[current_city][city]) ** BETA
                probabilities[city] = pheromone * visibility
                total += probabilities[city]

        # Normalisasi probabilitas
        if total > 0:
            probabilities = [p / total for p in probabilities]

        # Debugging: Tampilkan probabilitas
        print(f"    Dari kota {self.city_names[current_city]} ke:")
        for city, prob in enumerate(probabilities):
            if not visited[city]:
                print(f"        Kota {self.city_names[city]} memiliki probabilitas {prob:.4f}")

        # Pilih kota berdasarkan probabilitas
        r = random.random()  # Angka acak antara 0 dan 1
        print(f"\n    Nilai random (r): {r:.4f}")
        cumulative = 0.0
        for city in range(self.num_cities):
            if not visited[city]:
                cumulative += probabilities[city]
                if r <= cumulative:
                    print(f"        Kota {self.city_names[city]} dipilih (r <= kumulatif).\n")
                    return city

        return -1  # Jika semua kota telah dikunjungi

    def calculate_path_length(self, path):
        length = 0.0
        for i in range(len(path) - 1):
            length += self.distances[path[i]][path[i + 1]]
        length += self.distances[path[-1]][path[0]]  # Kembali ke kota awal
        return length

    def update_pheromones(self, ant_paths, ant_paths_length):
        # Evaporasi feromon
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                self.pheromones[i][j] *= (1.0 - RHO)

        # Tambahkan feromon berdasarkan panjang rute
        for path, path_length in zip(ant_paths, ant_paths_length):
            contribution = 1.0 / path_length
            for i in range(len(path) - 1):
                city1 = path[i]
                city2 = path[i + 1]
                self.pheromones[city1][city2] += contribution
                self.pheromones[city2][city1] += contribution
            # Kembali ke kota awal
            self.pheromones[path[-1]][path[0]] += contribution
            self.pheromones[path[0]][path[-1]] += contribution

    def draw_pheromones(self):
        print("\n===== Matriks Feromon =====")
        for row in self.pheromones:
            print(" ".join(f"{val:.4f}" for val in row))
        print("===========================")

    def draw_paths(self, ant_paths, ant_paths_length):
        print("\n===== Rute yang Ditempuh oleh Semut =====")
        for ant, path in enumerate(ant_paths):
            path_str = " -> ".join(self.city_names[city] for city in path)
            print(f"Semut ke-{ant + 1}: {path_str} -> {self.city_names[path[0]]} | Panjang rute: {ant_paths_length[ant]:.4f}")
        print("=========================================")

    def solve(self, start_city):
        best_path = []
        best_length = float("inf")
        best_lengths = []  # Untuk menyimpan jarak terbaik setiap iterasi

        for iteration in range(MAX_ITERATIONS):
            print(f"==================== Iterasi {iteration + 1} ====================")
            ant_paths = []
            ant_paths_length = []

            for ant in range(NUM_ANTS):
                print(f"\n************ Semut ke-{ant + 1} ************")
                visited = [False] * self.num_cities
                path = [start_city]
                visited[start_city] = True

                for _ in range(self.num_cities - 1):
                    current_city = path[-1]
                    next_city = self.select_next_city(current_city, visited)
                    path.append(next_city)
                    visited[next_city] = True

                path_length = self.calculate_path_length(path)
                ant_paths.append(path)
                ant_paths_length.append(path_length)

                # Tampilkan rute yang ditempuh
                print(f"    Rute yang ditempuh: {' -> '.join(self.city_names[city] for city in path)}")
                print(f"    Panjang rute: {path_length:.4f}")

                if path_length < best_length:
                    best_length = path_length
                    best_path = path

            best_lengths.append(best_length)
            self.update_pheromones(ant_paths, ant_paths_length)
            self.draw_pheromones()
            self.draw_paths(ant_paths, ant_paths_length)

        print("\n===== Hasil Akhir =====")
        print(f"Rute terbaik: {' -> '.join(self.city_names[city] for city in best_path)}")
        print(f"Jarak total: {best_length:.4f}")

        return best_lengths

# Data jarak antar kota
distances = [
    [0, 2790, 790, 1627, 2145, 96, 1781, 2777, 1374, 2565],
    [2790, 0, 2015, 1374, 373, 2713, 1202, 120, 1435, 340],
    [790, 2015, 0, 1085, 1753, 668, 1240, 2067, 967, 1833],
    [1627, 1374, 1085, 0, 1015, 1543, 197, 1304, 239, 1632],
    [2145, 373, 1753, 1015, 0, 2085, 982, 355, 888, 654],
    [96, 2713, 668, 1543, 2085, 0, 1570, 2697, 1300, 2483],
    [1781, 1202, 1240, 197, 982, 1570, 0, 1180, 274, 1465],
    [2777, 120, 2067, 1304, 355, 2697, 1180, 0, 1360, 415],
    [1374, 1435, 967, 239, 888, 1300, 274, 1360, 0, 1433],
    [2565, 340, 1833, 1632, 654, 2483, 1465, 415, 1433, 0]
]

city_names = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
]

# Tampilkan daftar kota
print("Daftar Kota:")
for i, city in enumerate(city_names):
    print(f"{i}. {city}")

# Input pengguna
start_city = int(input("\nMasukkan indeks kota awal (0 - 9): "))
while start_city < 0 or start_city >= len(city_names):
    print("Indeks tidak valid. Coba lagi.")
    start_city = int(input("\nMasukkan indeks kota awal (0 - 9): "))

# Jalankan algoritma
aco = ACO(distances, city_names)
best_lengths = aco.solve(start_city)

# Visualisasi hasil
iterations = list(range(1, len(best_lengths) + 1))
plt.plot(iterations, best_lengths, color="orange")
plt.title("Iterasi vs Jarak Terpendek")
plt.xlabel("Iterasi")
plt.ylabel("Jarak Terpendek")
plt.grid()

# Simpan grafik ke file untuk memastikan matplotlib berjalan
plt.savefig("plot 20 100.png")

# Tampilkan grafik
plt.show()

