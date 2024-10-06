import math
from models.Node import Node

class NodeController:
    '''
    Classe représentant un controlleur qui se charge des opérations sur les noeuds.

    Attributs:
        graph (Graph): Un graph représenté par des noeuds et liens, côté Model

    Méthodes:
        add_node(pos): Ajoute un noeud sur le graphe à partir d'un jeu de coordonnées (x, y).
        start_drag(pos): Initialise le déplacement en spécifiant le noeud qui est voué à être déplacé grâce à un jeu de coordonnées (x, y).
        end_drag(pos): Termine le déplacement en supprimant la spécification du noeud déplacé.
        drag_node(pos): Déplace le noeud grâce à la position (x, y) spécifiée par la souris de l'utilisateur.
        select_node(pos): Sélectionne un noeud par rapport à une position (x, y) spécifiée à la souris par l'utilisateur.
        clear_selection(pos): Supprime la référence du noeud sélectionné.
        get_node_at_position(pos): Cherche la référence d'un noeud en comparant ses coordonnées avec des coordonnées (x, y) spécifiées par la souris de l'utilisateur.
    '''
    def __init__(self, graph) -> None:
        self.graph = graph
        self.dragging_node = None
        self.selected_node = None

    def add_node(self, pos) -> None:
        '''
        Cette méthode ajoute un nouveau noeud dans le graphe.

        Args:
            pos (tuple de float): Coordonnées du clic de la souris
        '''
        self.graph.add_node(pos[0], pos[1])

    def start_drag(self, pos) -> None:
        '''
        Cette méthode initialise le déplacement d'un noeud en stockant sa référence.

        Args:
            pos (tuple de float): Coordonnées du clic de la souris
        '''
        self.dragging_node = self.get_node_at_position(pos)

    def end_drag(self) -> None:
        '''
        Cette méthode termine le déplacement d'un noeud en supprimant sa référence.
        '''
        self.dragging_node = None

    def drag_node(self, pos) -> None:
        '''
        Cette méthode se charge du déplacement d'un noeud à l'aide de la position du curseur de la souris.

        Args:
            pos (tuple de float): Coordonnées du curseur de la souris
        '''
        if self.dragging_node is not None:
            # On modifie les coordonnées du noeud que l'on déplace en fonction des coordonnées de la souris
            self.dragging_node.x, self.dragging_node.y = pos

    def select_node(self, pos) -> None:
        '''
        Cette méthode sélectionne un noeud grâce aux coordonnées (x, y) de la souris (s'il existe), destiné à créer des liens entre les noeuds.

        Args:
            pos (tuple de float): Coordonnées du clic de la souris
        '''
        node = self.get_node_at_position(pos)
        if node is not None:
            # Si le noeud, dont les coordonnées du clic de la souris a été réalisé, existe, alors on le récupère
            self.selected_node = node
        else:
            self.selected_node = None

    def clear_selection(self) -> None:
        '''
        Cette méthode désélectionne le noeud actuellement sélectionné. Elle est appelée lorsque l'utilisateur ne souhaite plus établir de lien entre deux noeuds.
        '''
        self.selected_node = None

    def get_node_at_position(self, pos) -> None|Node:
        '''
        Cette méthode retourne le noeud correspondant aux coordonnées du clic de l'utilisateur. Le nœud est identifié par ses coordonnées qui correspondent à celles du clic effectué.
        '''
        for node in self.graph.nodes:
            # TODO : modifier 10 par la largeur du noeud (ajouter un lien donc avec le Model noeud & ajouter une épaisseur de noeud directement dans le model)
            if math.sqrt((node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2) < 10:
                return node
        return None
