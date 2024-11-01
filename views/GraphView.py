import pygame
from models.Graph import Graph
from constants.Colors import Colors
from constants.Config import NODE_RADIUS

class GraphView:
    def __init__(self, screen, background_image) -> None:
        # Stockage de l'écran (possédant les propriétés de largeur et hauteur)
        self.screen = screen
        # De même pour l'image de fond
        self.background_image = background_image

    def draw_graph(self, graph: Graph, selected_node=None, dragging_node=None) -> None:
        '''
        Cette méthode dessine l'interface utilisateur sur laquelle l'utilisateur conçoit son graphe.

        Args:
            graph (Graph): Graphe possédant les informations de l'intégralité des positions des noeuds et des edges (côté Model)
            selected_node (Node): Noeud sélectionné sur le graphe par l'utilisateur grâce au clique gauche
            dragging_node (Node): Noeud bougé par l'utilisateur lorsqu'il souhaite déplacer ce dernier
        '''
        # Affichage du plan du musée en fond
        if self.background_image is not None:
            self.screen.blit(self.background_image, (0, 0))

        # Dessin des noeuds
        for node in graph.nodes:
            if node == selected_node:
                color = Colors.SELECTED_NODE_COLOR.value
            elif node == dragging_node:
                color = Colors.DRAGGING_NODE_COLOR.value
            else:
                color = Colors.NODE_COLOR.value
            pygame.draw.circle(self.screen, color, (node.x, node.y), NODE_RADIUS)

        # Dessin des edges
        for edge in graph.edges:
            start_node = edge[0]
            end_node = edge[1]
            pygame.draw.line(self.screen, Colors.EDGE_COLOR.value, (start_node.x, start_node.y), (end_node.x, end_node.y), 3)

    def draw_simulation(self, agents):
        """Dessine chaque agent à sa position mise à jour"""

        for i, agent in enumerate(agents):
            pygame.draw.circle(self.screen, Colors.AGENT_COLOR.value, (int(agent.x), int(agent.y)), 5)


    def has_an_image(self) -> bool:
        return self.background_image is not None