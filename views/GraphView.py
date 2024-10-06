import pygame
from models.Graph import Graph
from constants.Colors import Colors

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
            selected_node (Bool): Noeud sélectionné sur le graphe par l'utilisateur grâce au clique gauche
        '''
        # Affichage du plan du musée en fond
        self.screen.blit(self.background_image, (0, 0))

        # Dessin des noeuds
        for node in graph.nodes:
            if node == selected_node:
                color = Colors.SELECTED_NODE_COLOR.value
            elif node == dragging_node:
                color = Colors.DRAGGING_NODE_COLOR.value
            else:
                color = Colors.NODE_COLOR.value
            pygame.draw.circle(self.screen, color, (node.x, node.y), 10)

        # Dessin des edges
        for edge in graph.edges:
            start_node = edge[0]
            end_node = edge[1]
            pygame.draw.line(self.screen, Colors.BLACK.value, (start_node.x, start_node.y), (end_node.x, end_node.y), 3)
        
