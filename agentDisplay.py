import pygame
import numpy as np

pygame.init()

# dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
NODE_RADIUS = 5

# couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AGENT_COLOR = (0, 255, 0)
EDGE_COLOR = (150, 150, 150)

# graphe fixe (à modif + tard)
nodes = [(80, 120), (160, 200), (300, 150), (450, 100), (550, 200),
         (100, 450), (250, 500), (400, 400), (500, 500), (550, 350)]

# matrice des arêtes (1 = connecté, 0 = non connecté)
adjacency_matrix = np.array([
    [0, 1, 1, 0, 0, 1, 0, 0, 0, 0],  # Connexions du noeud 0
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # Connexions du noeud 1
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 0],  # Connexions du noeud 2
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],  # Connexions du noeud 3
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 1],  # Connexions du noeud 4
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # Connexions du noeud 5
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],  # Connexions du noeud 6
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0],  # Connexions du noeud 7
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 1],  # Connexions du noeud 8
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0]  # Connexions du noeud 9
])


# classe pour représenter un agent
class Agent:
    def __init__(self, current_node):
        self.current_node = self.target_node = current_node
        self.x, self.y = self.target_x, self.target_y = nodes[current_node]
        self.speed = 2  # Vitesse de déplacement en pixels

    def move(self):
        # si l'agent est arrivé à destination, choisir un nouveau nœud adjacent
        if self.x == self.target_x and self.y == self.target_y:
            neighbors = np.where(adjacency_matrix[self.current_node] == 1)[0]  # nœuds voisins
            self.target_node = np.random.choice(neighbors)  # choisir un voisin aléatoire
            self.target_x, self.target_y = nodes[self.target_node]

        # déplacement de l'agent le long de l'arête
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = np.sqrt(dx ** 2 + dy ** 2) #Pythagore

        if distance != 0:
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

        # si l'agent atteint le nœud cible, mettre à jour le nœud actuel
        if abs(self.x - self.target_x) < self.speed and abs(self.y - self.target_y) < self.speed:
            self.x, self.y = self.target_x, self.target_y
            self.current_node = self.target_node


# dessiner le graphe
def draw_graph(screen, nodes, adjacency_matrix):
    # arêtes
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if adjacency_matrix[i][j] == 1:
                pygame.draw.line(screen, EDGE_COLOR, nodes[i], nodes[j], 2)

    # noeuds
    for node in nodes:
        pygame.draw.circle(screen, BLACK, node, NODE_RADIUS)


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Agents sur graphe fixe")

    clock = pygame.time.Clock()  # Pour contrôler les FPS

    # création de plusieurs agents, chaque agent commence à un nœud aléatoire
    num_agents = 5
    agents = [Agent(np.random.randint(0, len(nodes))) for _ in range(num_agents)]

    while True:
        screen.fill(WHITE)
        if pygame.QUIT in [event.type for event in pygame.event.get()]:
            break
        # dessiner le graphe
        draw_graph(screen, nodes, adjacency_matrix)
        # déplacer et dessiner les agents
        for agent in agents:
            agent.move()
            pygame.draw.circle(screen, AGENT_COLOR, (int(agent.x), int(agent.y)), NODE_RADIUS)
        pygame.display.flip()
        # contrôler les FPS
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
