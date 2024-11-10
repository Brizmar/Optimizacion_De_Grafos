# Implementacion de el Algoritmo de Dijkstra en Python

import heapq

class Nodo:
    # Constructor, inicializa los atributos que tendra un nodo
    def __init__(self, indice, distancia):
        self.indice = indice
        self.distancia = distancia
    
    # Metodo que permite comparar nodos por distancia
    def __lt__(self, other):
        return self.distancia < other.distancia

# Funcion Dijkstra
# nodos = numero total de nodos en el grafo
# adj = lista de adyacencia que representa el grafo
# nodo_origen = nodo de origen
def Dijkstra(nodos, adyacencia, nodo_origen):
    # Inicializacion de estructuras
    visitados = [False] * nodos      # lista de nodos visitados            
    map = {}                         # diccionario -> ¿de donde llego? y ¿cuanto recorrio desde el nodo de origen?
    q = []                           # cola de prioridad 

    # Inicializacion del nodo de origen
    # nodo_origen se establece con una distancia de 0
    map[nodo_origen] = Nodo(nodo_origen, 0)
    heapq.heappush(q, Nodo(nodo_origen, 0))

    # Procesamiento de la cola de prioridad
    while q:
        n = heapq.heappop(q)
        indice = n.indice
        distancia = n.distancia
        visitados[indice] = True

        # Actualizacion de distancias para vecinos
        adyList = adyacencia[indice]
        for adyLink in adyList:
            vecino, peso = adyLink
            if not visitados[vecino]:
                if vecino not in map:
                    map[vecino] = Nodo(indice, distancia + peso)
                else:
                    sn = map[vecino]
                    if distancia + peso < sn.distancia:
                        sn.indice = indice
                        sn.distancia = distancia + peso
                heapq.heappush(q, Nodo(vecino, distancia + peso))

    # Preparacion del resultado final
    resultado = [float('inf')] * nodos  # Inicializa con inf para nodos no alcanzables
    for i in range(nodos):
        if i in map:
            resultado[i] = map[i].distancia

    return resultado

# Funcion main
def main():
    adyacencia = [[] for _ in range(6)]

    nodos = 6
    aristas = 5
    u = [0, 0, 1, 2, 4]
    indice = [3, 5, 4, 5, 5]
    w = [9, 4, 4, 10, 3]

    # Creacion de la lista de adyacencia
    for i in range(aristas):
        edge = [indice[i], w[i]]
        adyacencia[u[i]].append(edge)

        edge2 = [u[i], w[i]]
        adyacencia[indice[i]].append(edge2)

    # Ejecucion de algoritmo y visualizacion de resultados
    nodo_origen = 1

    resultado = Dijkstra(nodos, adyacencia, nodo_origen)
    print(resultado)

if __name__ == "__main__":
    main()