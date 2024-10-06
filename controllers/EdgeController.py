from controllers.NodeController import NodeController
from models.Graph import Graph

class EdgeController:
    '''
    Classe représentant un controlleur qui se charge des opérations de liens entre les noeuds.

    Attributs:
        graph (Graph): Un graph représenté par des noeuds et liens, côté Model
        node_controller (NodeController): Une référence du controlleur de noeuds

    Méthodes:
        create_link(pos): Crée un lien entre deux noeuds à partir d'une position de coordonnées (x, y) et le noeud précédemment sélectionné.
    '''
    def __init__(self, graph: Graph, node_controller: NodeController):
        self.graph = graph
        self.node_controller = node_controller

    def create_link(self, pos):
        """
        Cette méthode crée un lien entre deux noeuds, grâce à la récupération d'un noeud à partir d'un jeu de coordonnées (x,y) et l'ancien noeud précédemment sélectionné.

        Args:
            pos (tuple de float): position du clic de la souris
        
        Cette méthode ne retourne rien.
        """
        node = self.node_controller.get_node_at_position(pos)
        # Si le noeud est bien sélectionné, que le second noeud avec lequel on souhaite créer le lien existe et que les deux noeuds ne sont pas identiques:
        if self.node_controller.selected_node is not None and node is not None and self.node_controller.selected_node != node:
            # On ajoute un lien
            self.graph.add_edge(self.node_controller.selected_node, node)
            self.node_controller.selected_node = None

    