import pygame
from models.Graph import Graph
from views.GraphView import GraphView
from controllers.NodeController import NodeController
from controllers.EdgeController import EdgeController

from services.ICSVService import ICSVService

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, NODE_RADIUS

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
     
    def __init__(self, screen, csv_service: ICSVService) -> None:
        # Stockage de l'instanciation du model de graph (nécessaire pour le lien entre vue et model)
        self.graph = Graph()
        
        # TODO : Chargement dynamique d'image, cf. Arnaud
        self.image_path = "image1.jpg"
        background_image = pygame.image.load(self.image_path)
        # Mise à jour des dimensions de l'image d'arrière plan par rapport à la taille de la fenêtre de graph
        background_image = pygame.transform.scale(background_image, (GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.graph_view = GraphView(screen.subsurface((0, 0, GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)), background_image)

        # Le controlleur GraphController décompose son champ d'action grâce à l'aggrégation de nouveaux controlleurs :
        self.node_controller = NodeController(self.graph)
        self.edge_controller = EdgeController(self.graph, self.node_controller)

        # Injection de dépendance du service de CSV
        self.csv_service = csv_service

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

        if event.type == pygame.MOUSEBUTTONDOWN :
            node = self.node_controller.get_node_at_position(pos)
            if event.button == 1:
                self.handle_left_click(pos, node)

            # S'il s'agit du clic droit :
            elif event.button == 3:
                self.handle_right_click(pos, node)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.node_controller.end_drag()

        # On vérifie que le déplacement (drag) du bouton ne dépasse pas les limites de la fenêtre du graphe
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if pos[0] < GRAPH_WINDOW_WIDTH  - NODE_RADIUS and pos[1] < GRAPH_WINDOW_HEIGHT - NODE_RADIUS and pos[0] > NODE_RADIUS and pos[1] > NODE_RADIUS:
                self.node_controller.drag_node(pos)

    def handle_left_click(self, pos, node) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            self.node_controller.delete_node(node)
        else:
            # On clear l'éventuelle sélection de création de lien
            self.node_controller.clear_selection()
            # On initialise le potentiel déplacement du noeud grâce au controller Node
            self.node_controller.start_drag(pos)
            # Si le clic est réalisé sur une position où aucun noeud n'est présent,
            if node is None:
                # On en crée un nouveau
                if pos[0] < GRAPH_WINDOW_WIDTH - NODE_RADIUS and pos[1] < GRAPH_WINDOW_HEIGHT - NODE_RADIUS:
                    self.node_controller.add_node(pos)

    def handle_right_click(self, pos, node) -> None:
        # On crée un lien grâce au controller Edge
        self.edge_controller.create_link(pos)

        self.node_controller.select_node(node)

    def update(self) -> None:
        """
        Cette méthode met à jour l'affichage du graphe.
        
        Elle ne prend pas d'arguments et ne retourne rien.
        """
        self.graph_view.draw_graph(self.graph, self.node_controller.selected_node, self.node_controller.dragging_node)

    def save_graph(self) -> None:
        edges_matrix, nodes_list = self.graph.compute_matrix()
        self.csv_service.save(edges_matrix, nodes_list, self.image_path)

    def load_graph(self, num_file) -> None:
        edges_matrix, nodes_list = self.csv_service.load(num_file)
        if edges_matrix and nodes_list:
            self.graph.nodes = {i: coords for i, coords in enumerate(nodes_list)}

    def clear_graph(self) -> None:
        self.graph.nodes.clear()
        self.graph.edges.clear()

    def graph_has_an_image(self) -> bool:
        return self.graph_view.has_an_image()