import matplotlib.pyplot as plt
import networkx as nx
import time

# Clase para representar un grafo
class Grafo:

    def __init__(self, vertices):
        self.V = vertices
        self.grafo = []

    # Función para agregar una arista al grafo
    def agregarArista(self, u, v, w):
        self.grafo.append([u, v, w])

    # Una función auxiliar para encontrar el conjunto de un elemento i (compresión de caminos)
    def encontrar(self, padre, i):
        if padre[i] != i:
            padre[i] = self.encontrar(padre, padre[i])
        return padre[i]

    # Unión de dos conjuntos de x y y (con unión por rango)
    def union(self, padre, rango, x, y):
        if rango[x] < rango[y]:
            padre[x] = y
        elif rango[x] > rango[y]:
            padre[y] = x
        else:
            padre[y] = x
            rango[x] += 1

    # La función principal para construir el MST utilizando el algoritmo de Kruskal
    def KruskalMST(self):
        resultado = []
        i = 0
        e = 0

        # Ordenar todas las aristas en orden no decreciente de su peso
        self.grafo = sorted(self.grafo, key=lambda item: item[2])

        padre = []
        rango = []

        for nodo in range(self.V):
            padre.append(nodo)
            rango.append(0)

        # Crear el grafo inicial en NetworkX para visualización
        G = nx.Graph()
        for u, v, w in self.grafo:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G)  # Layout fijo para que el grafo no cambie de posición
        plt.ion()  # Activar modo interactivo

        # Dibujar el grafo inicial
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Grafo Inicial")
        plt.show()
        time.sleep(2)

        while e < self.V - 1:
            u, v, w = self.grafo[i]
            i += 1
            x = self.encontrar(padre, u)
            y = self.encontrar(padre, v)

            if x != y:
                e += 1
                resultado.append((u, v, w))
                self.union(padre, rango, x, y)

                # Dibujar el grafo en el paso actual
                plt.clf()  # Limpiar la figura actual para el siguiente paso
                nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_weight='bold')
                labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

                # Dibujar aristas con colores: rojo para la arista actual y verde para las que están en el MST
                edge_colors = []
                for edge in G.edges():
                    if (edge[0], edge[1], G[edge[0]][edge[1]]['weight']) in resultado:
                        edge_colors.append('green')
                    elif (edge[0], edge[1]) == (u, v) or (edge[1], edge[0]) == (u, v):
                        edge_colors.append('red')
                    else:
                        edge_colors.append('black')
                
                nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
                
                plt.title(f"Paso {e}: Agregando arista {u} -- {v} con peso {w}")
                plt.draw()
                plt.pause(2)  # Pausar para ver el paso actual

        plt.ioff()  # Desactivar modo interactivo
        plt.show()

        # Resultado final
        costoMinimo = sum(weight for u, v, weight in resultado)
        print("Aristas en el MST construido")
        for u, v, peso in resultado:
            print(f"{u} -- {v} == {peso}")
        print("Costo minimo del Arbol de Expansion Minima:", costoMinimo)


# Código principal
if __name__ == '__main__':
    g = Grafo(4)
    g.agregarArista(0, 1, 10)
    g.agregarArista(0, 2, 6)
    g.agregarArista(0, 3, 5)
    g.agregarArista(1, 3, 15)
    g.agregarArista(2, 3, 4)

    # Llamada a la función
    g.KruskalMST()
