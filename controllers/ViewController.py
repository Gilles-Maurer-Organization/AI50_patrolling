import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH

from views.GraphView import GraphView
from controllers.GraphController import GraphController
from views.ParametersView import ParametersView
from controllers.ParametersController import ParametersController

from services.ICSVService import ICSVService

class ViewController:
    def __init__(self, csv_service: ICSVService) -> None:
        self.screen = pygame.display.set_mode((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.graph_controller = GraphController(self.screen, csv_service)
        self.parameters_controller = ParametersController(self.screen, self.graph_controller)
        self.parameters_view = ParametersView(self.screen)

    def handle_actions(self, event) -> None:
        self.parameters_controller.handle_events(event)
        self.graph_controller.handle_event(event)

    def draw(self) -> None:
        '''
        Cette méthode dessine tous les paramètres et la vue de graph.
        '''
        self.parameters_controller.draw_parameters()
        self.graph_controller.update()
