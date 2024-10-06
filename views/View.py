import pygame
from views.GraphView import GraphView
from views.ParametersView import ParametersView

class View:
    def __init__(self) -> None:
        # Dimensions de la fenêtre (1/2 de 1920 par 1080)
        WIDTH, HEIGHT = 960, 540
        screen = pygame.display.set_mode((WIDTH + 300, HEIGHT))

        # Chargement de l'image d'arrière plan
        # TODO : Chargement dynamique, cf. Arnaud
        background_image = pygame.image.load("image1.jpg")
        # Mise à jour des dimensions de l'image d'arrière plan par rapport à la taille de la fenêtre de graph
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        self.screen = screen

        # Création de la vue Graphe
        self.graph_view = GraphView(screen.subsurface((0, 0, WIDTH, HEIGHT)), background_image)

        # Création de la vue paramètres
        self.parameters_view = ParametersView(screen.subsurface((WIDTH, 0, 300, HEIGHT)))
        

    def get_graphView(self) -> GraphView:
        return self.graph_view
    
    def draw(self) -> None:
        self.parameters_view.draw_parameters()
