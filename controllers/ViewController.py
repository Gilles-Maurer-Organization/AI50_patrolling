import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH

from views.GraphView import GraphView
from controllers.GraphController import GraphController
from views.ParametersView import ParametersView

class ViewController:
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH + PARAMETERS_WINDOW_WIDTH, self.HEIGHT))
        self.graph_controller = GraphController(self.WIDTH, self.HEIGHT, self.screen)
        self.parameters_view = ParametersView(self.screen.subsurface((self.WIDTH, 0, PARAMETERS_WINDOW_WIDTH, self.HEIGHT)), self.graph_controller)
       
    def handle_actions(self, event) -> None:
        self.parameters_view.handle_events(event)
        self.graph_controller.handle_event(event)

    def draw(self) -> None:
        '''
        Cette méthode dessine tous les paramètres et la vue de graph.
        '''
        self.parameters_view.draw_parameters()
        self.graph_controller.update()
