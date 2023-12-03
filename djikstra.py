import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors

class Dijkstra:
    def __init__(self, graph):
        # Inisialisasi objek Dijkstra dengan graf sebagai parameter
        self.graph = graph
        # Membuat objek Node untuk setiap node dalam graf
        for name, neighbors in graph.items():
            graph[name] = Node(name, neighbors)

    def find_shortest_path(self, start_node, end_node):
        # Inisialisasi jarak ke setiap node sebagai tak terhingga
        distance = {node: float('inf') for node in self.graph}
        # Inisialisasi node pendahulu ke setiap node sebagai None
        predecessor = {node: None for node in self.graph}
        # Jarak dari start_node ke dirinya sendiri diatur sebagai 0
        distance[start_node] = 0
        # Antrian untuk menyimpan pasangan jarak-node yang akan dieksplorasi
        queue = [(0, start_node)]
        
        # Algoritma Dijkstra
        while queue:
            current_distance, current_node = min(queue)
            queue.remove((current_distance, current_node))

            for neighbor, weight in self.graph[current_node].neighbors.items():
                new_distance = current_distance + weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    predecessor[neighbor] = current_node
                    queue.append((new_distance, neighbor))

        # Mendapatkan jarak terpendek dari start_node ke end_node
        shortest_distance = distance[end_node]
        if shortest_distance == float('inf'):
            return None  # Tidak ada jalur yang ditemukan

        # Membuat jalur dari end_node ke start_node
        path = [end_node]
        while path[-1] != start_node:
            path.append(predecessor[path[-1]])

        return path[::-1]

def visualize_graph_with_highlighted_path(graph, shortest_path):
    # Membuat objek graf dari NetworkX
    G = nx.DiGraph()
    # Menambahkan node dan edge ke graf
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    # Menentukan posisi node dalam graf
    pos = nx.spring_layout(G)
    # Menggambar graf dengan label node, warna, dan ukuran node
    nx.draw(G, pos, with_labels=True, node_size=720, node_color='#acb0be', font_size=15)

    if shortest_path:
        # Jika ada jalur terpendek, visualisasikan dengan warna yang berbeda
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='#f38ba8', node_size=960)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#eba0ac', width=2.5,arrows=True ,arrowstyle='-|>' )

        # Menambahkan label berat pada setiap edge
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Menampilkan plot graf
    plt.show()

def main():
    # Definisi graf
    graph = {
        'A': {'B':16, 'C':3, 'D':10},
        'B': {'D':2,'I':8},
        'C': {'B':12,'E':7},
        'D': {'F':6},
        'E': {'G':5},
        'F': {'I':6},
        'G': {'I':8},
        'I': {},
    }
    # Node awal dan akhir untuk mencari jalur terpendek
    start_node = 'A'
    end_node = 'I'

    # Membuat objek Dijkstra
    dijkstra_algorithm = Dijkstra(graph)
    # Mencari jalur terpendek dari start_node ke end_node
    shortest_path = dijkstra_algorithm.find_shortest_path(start_node, end_node)

    # Menampilkan hasil jalur terpendek
    if shortest_path:
        print(f"Shortest path from {start_node} to {end_node}: {' -> '.join(shortest_path)}")
    else:
        print(f"No path found from {start_node} to {end_node}")

    # Visualisasi graf dengan jalur terpendek yang disorot
    visualize_graph_with_highlighted_path(graph, shortest_path)

if __name__ == "__main__":
    main()
