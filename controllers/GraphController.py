import pygame
from models import Graph
from views import GraphView
from controllers.NodeController import NodeController
from controllers.EdgeController import EdgeController
from controllers.CSVController import CSVController

class GraphController:
    '''
    Classe représentant un controlleur qui se charge des opérations du graphe entier.

    Attributs:
        graph (Graph): Un graph représenté par des noeuds et liens, côté Model
        graph_view (GraphView): Une référence de la vue du graphe

    Méthodes:
        handle_event(event): Manage les événements du clic de souris de l'utilisateur lors de la création de son graphe.
        update(): Met à jour l'affichage du graphe.
        save_graph(): Sauvegarde le graphe crée par l'utilisateur.
        load_graph(): Charge un graphe déjà existant sous format csv.
    '''
     
    def __init__(self, graph: Graph, graph_view: GraphView) -> None:
        # Stockage de l'instanciation du model de graph (nécessaire pour le lien entre vue et model)
        self.graph = graph
        # Il en va de même pour le stockage de l'instanciation du graph côté view
        self.graph_view = graph_view

        # Le controlleur GraphController décompose son champ d'action grâce à l'aggrégation de nouveaux controlleurs :
        self.node_controller = NodeController(graph)
        self.edge_controller = EdgeController(graph, self.node_controller)
        self.csv_controller = CSVController()

    def handle_event(self, event) -> None:
        '''
        Cette méthode gère les événements générés par la souris de l'utilisateur.

        Args:
            event (pygame.event.Event): L'événement généré, qui peut inclure
            des informations sur le type d'événement (par exemple,
            MOUSEBUTTONDOWN, MOUSEBUTTONUP, etc.) ainsi que des données
            supplémentaires (comme la position de la souris).
        '''

        # Récupération de la position de la souris
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # TODO : récupérer le noeud directement grâce à la méthode get_node_at_position() de la classe NodeController
            # plutot que de le faire à chaque fois dans start_drag, add_node, etc

            # S'il s'agit du clic gauche :
            if event.button == 1:
                # On clear l'éventuelle sélection de création de lien
                self.node_controller.clear_selection()
                # On initialise le potentiel déplacement du noeud grâce au controller Node
                self.node_controller.start_drag(pos)
                # Si le clic est réalisé sur une position où aucun noeud n'est présent,
                if self.node_controller.get_node_at_position(pos) is None:
                    # On en crée un nouveau
                    self.node_controller.add_node(pos)

            # S'il s'agit du clic droit :
            elif event.button == 3:
                # On crée un lien grâce au controller Edge
                self.edge_controller.create_link(pos)

                self.node_controller.select_node(pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.node_controller.end_drag()

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                self.node_controller.drag_node(pos)

    def update(self) -> None:
        """
        Cette méthode met à jour l'affichage du graphe.
        
        Elle ne prend pas d'arguments et ne retourne rien.
        """
        self.graph_view.draw_graph(self.graph, self.node_controller.selected_node, self.node_controller.dragging_node)

    def save_graph(self) -> None:
        edges_matrix, nodes_list = self.graph.compute_matrix()
        self.csv_controller.save(edges_matrix, nodes_list)

    def load_graph(self, num_file) -> None:
        edges_matrix, nodes_list = self.csv_controller.load(num_file)
        if edges_matrix and nodes_list:
            self.graph.nodes = {i: coords for i, coords in enumerate(nodes_list)}

