import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, **neighbors):
        self.name = name
        self.neighbors = {neighbor: weight for neighbor, weight in neighbors.items()}

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def find_shortest_path(self, start_node, end_node):
        distance = {node: float('inf') for node in self.graph}
        predecessor = {node: None for node in self.graph}
        distance[start_node] = 0
        queue = [(0, start_node)]
        while queue:
            current_distance, current_node = min(queue)
            queue.remove((current_distance, current_node))

            for neighbor, weight in self.graph[current_node].neighbors.items():
                new_distance = current_distance + weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    predecessor[neighbor] = current_node
                    queue.append((new_distance, neighbor))

        distance, predecessor = distance, predecessor
        shortest_distance = distance[end_node]
        if shortest_distance == float('inf'):
            return None  

        path = [end_node]
        while path[-1] != start_node:
            path.append(predecessor[path[-1]])

        return path[::-1]



def visualize_graph_with_highlighted_path(graph, shortest_path):
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightgray', font_size=15)

    if shortest_path:
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='yellow', node_size=800)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5, arrowstyle='-|>')

        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()

def main():
    graph = {
        'A': Node('A', B=1, C=4),
        'B': Node('B', D=2),
        'C': Node('C', D=6, F=3),
        'D': Node('D',  E=8),
        'E': Node('E'),
        'F': Node('F'),
    }

    start_node = 'A'
    end_node = 'E'

    dijkstra_algorithm = Dijkstra(graph)
    shortest_path = dijkstra_algorithm.find_shortest_path(start_node, end_node)

    if shortest_path:
        print(f"Shortest path from {start_node} to {end_node}: {' -> '.join(shortest_path)}")
    else:
        print(f"No path found from {start_node} to {end_node}")

    visualize_graph_with_highlighted_path(graph, shortest_path)

if __name__ == "__main__":
    main()
