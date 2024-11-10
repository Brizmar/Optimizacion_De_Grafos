import pygame
import heapq
import time

# Configuración inicial de Pygame y parámetros
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación del Algoritmo de Dijkstra")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

# Clase Nodo
class Nodo:
    def __init__(self, indice, distancia):
        self.indice = indice
        self.distancia = distancia
    
    def __lt__(self, other):
        return self.distancia < other.distancia

# Algoritmo de Dijkstra con visualización pausada
def Dijkstra(nodos, adyacencia, nodo_origen):
    visitados = [False] * nodos
    map = {}
    q = []
    map[nodo_origen] = Nodo(nodo_origen, 0)
    heapq.heappush(q, Nodo(nodo_origen, 0))

    while q:
        n = heapq.heappop(q)
        indice = n.indice
        distancia = n.distancia
        visitados[indice] = True

        draw_nodes_and_edges(adyacencia, visitados, map, nodo_origen, indice)
        pygame.display.flip()
        
        # Espera a que el usuario presione ESPACIO para el siguiente paso
        wait_for_space()

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
                draw_nodes_and_edges(adyacencia, visitados, map, nodo_origen, vecino)
                pygame.display.flip()
                wait_for_space()

    resultado = [float('inf')] * nodos
    for i in range(nodos):
        if i in map:
            resultado[i] = map[i].distancia
    return resultado

# Dibujo de nodos, aristas y detalles
def draw_nodes_and_edges(adyacencia, visitados, map, nodo_origen, nodo_actual):
    screen.fill(WHITE)
    node_positions = [(100, 100), (200, 200), (300, 100), (400, 200), (500, 100), (600, 200)]
    font = pygame.font.Font(None, 24)
    
    # Dibujar aristas con pesos
    for i, edges in enumerate(adyacencia):
        for (j, peso) in edges:
            pygame.draw.line(screen, GRAY, node_positions[i], node_positions[j], 2)
            text = font.render(str(peso), True, BLACK)
            mid_point = ((node_positions[i][0] + node_positions[j][0]) // 2, (node_positions[i][1] + node_positions[j][1]) // 2)
            screen.blit(text, mid_point)

    # Dibujar nodos con estado visual
    for i, (x, y) in enumerate(node_positions):
        color = GREEN if visitados[i] else RED if i == nodo_actual else BLUE if i == nodo_origen else GRAY
        pygame.draw.circle(screen, color, (x, y), 20)
        distancia = map[i].distancia if i in map else float('inf')
        text = font.render(f"{distancia}", True, BLACK)
        screen.blit(text, (x - 10, y - 10))
    
    pygame.display.flip()

# Botón de inicio
def draw_start_button():
    font = pygame.font.Font(None, 36)
    text = font.render("INICIAR", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    color = BUTTON_COLOR if not button_hovered(button_rect) else BUTTON_HOVER_COLOR
    pygame.draw.rect(screen, color, button_rect)
    screen.blit(text, (button_rect.x + 15, button_rect.y + 10))
    return button_rect

def button_hovered(button_rect):
    mouse_pos = pygame.mouse.get_pos()
    return button_rect.collidepoint(mouse_pos)

def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        clock.tick(30)

# Configuración del grafo
def main():
    adyacencia = [[] for _ in range(6)]
    nodos = 6
    aristas = 5
    u = [0, 0, 1, 2, 4]
    v = [3, 5, 4, 5, 5]
    w = [9, 4, 4, 10, 3]

    for i in range(aristas):
        edge = [v[i], w[i]]
        adyacencia[u[i]].append(edge)
        edge2 = [u[i], w[i]]
        adyacencia[v[i]].append(edge2)

    nodo_origen = 1
    simulation_started = False

    # Ciclo de Pygame con botón de inicio
    running = True
    while running:
        screen.fill(WHITE)
        
        # Mostrar botón de inicio antes de que comience la simulación
        if not simulation_started:
            button_rect = draw_start_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not simulation_started:
                if button_rect.collidepoint(event.pos):
                    simulation_started = True
                    Dijkstra(nodos, adyacencia, nodo_origen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
