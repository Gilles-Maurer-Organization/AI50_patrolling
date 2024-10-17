import pygame


from views.GraphView import GraphView
from views.ParametersView import ParametersView

class View:
    def __init__(self) -> None:
        # Dimensions de la fenêtre (1/2 de 1920 par 1080)
        self.WIDTH, self.HEIGHT = 960, 540
        self.screen = pygame.display.set_mode((self.WIDTH + 310, self.HEIGHT))

    def initialize_graph_view(self) -> None:
        '''
        Cette méthode initialise la vue de graphe avec une image de fond.
        TODO : Supprimer l'initialisation actuelle de l'image de background pour par la suite l'incorporer dynamiquement depuis les paramètres.
        '''
        # Création de la vue Graphe

        # Chargement de l'image d'arrière plan
        # TODO : Chargement dynamique, cf. Arnaud
        background_image = pygame.image.load("image1.jpg")
        # Mise à jour des dimensions de l'image d'arrière plan par rapport à la taille de la fenêtre de graph
        background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))
        self.graph_view = GraphView(self.screen.subsurface((0, 0, self.WIDTH, self.HEIGHT)), background_image)

    def initialize_parameters_view(self, graph_controller) -> None:
        '''
        Cette méthode initialise la vue de paramètres.

        Args:
            graph_controller: Une référence du contrôleur du graphe afin de réaliser des opérations de sauvegarde, import, nettoyage, etc entre les deux vues.
        '''
        # Création de la vue paramètres
        self.parameters_view = ParametersView(self.screen.subsurface((self.WIDTH, 0, 310, self.HEIGHT)), graph_controller)

    def get_graphView(self) -> GraphView:
        return self.graph_view
    
    def get_parametersView(self) -> ParametersView:
        return self.parameters_view

    def draw(self, graph_controller) -> None:
        '''
        Cette méthode dessine tous les paramètres et la vue de graph.
        '''
        self.parameters_view.draw_parameters()
        graph_controller.update()
