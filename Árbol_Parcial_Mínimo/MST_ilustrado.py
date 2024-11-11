import sys
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        self.G = nx.Graph()  # Crea un grafo con NetworkX

    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight
        self.G.add_edge(u, v, weight=weight)  # Agrega la arista al grafo de NetworkX

    def min_key(self, key, mst_set):
        min_val = sys.maxsize
        min_index = -1
        for v in range(self.V):
            if key[v] < min_val and not mst_set[v]:
                min_val = key[v]
                min_index = v
        return min_index

    def draw_graph(self, mst_edges, step):
        pos = nx.spring_layout(self.G)
        plt.figure(figsize=(8, 6))

        # Dibuja todas las aristas con color gris
        nx.draw(self.G, pos, with_labels=True, node_color='yellow', edge_color='gray', node_size=700, font_weight='bold')
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)

        # Dibuja las aristas seleccionadas para MST con color rojo
        nx.draw_networkx_edges(self.G, pos, edgelist=mst_edges, edge_color='red', width=2)

        plt.title(f"Step {step}: Current MST edges")
        plt.savefig(f"MST_Paso_{step}.png")  # Guarda la imagen
        plt.close()

    def prim_mst(self):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        key[0] = 0
        mst_set = [False] * self.V
        mst_edges = []

        parent[0] = -1  # La raíz no tiene padre

        for count in range(self.V):
            u = self.min_key(key, mst_set)
            mst_set[u] = True

            # Agrega la arista al MST (excluyendo la raíz)
            if parent[u] != -1:  # Cambiado de None a -1
                mst_edges.append((parent[u], u))
            
            # Dibuja el grafo en el paso actual
            self.draw_graph(mst_edges, count + 1)

            for v in range(self.V):
                if self.graph[u][v] > 0 and not mst_set[v] and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u

# Código de prueba
if __name__ == '__main__':
    g = Graph(9)
    edges = [
        (0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7),
        (2, 5, 4), (2, 8, 2), (3, 4, 9), (3, 5, 14), (4, 5, 10),
        (5, 6, 2), (6, 7, 1), (6, 8, 6), (7, 8, 7)
    ]
    for u, v, weight in edges:
        g.add_edge(u, v, weight)

    g.prim_mst()