import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH

from controllers.FileExplorerController import FileExplorerController
from controllers.GraphController import GraphController
from controllers.ParametersController import ParametersController
from controllers.SimulationController import SimulationController
from services import IImageService

from services.CompleteGraphService import CompleteGraphService
from services.ICSVService import ICSVService

class ViewController:
    def __init__(self, csv_service: ICSVService, image_service: IImageService) -> None:
        self.screen = pygame.display.set_mode((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.graph_controller = GraphController(self.screen, csv_service, image_service)
        self.file_explorer_controller = FileExplorerController(self.screen, self.graph_controller)
        self.simulation_controller = SimulationController(self.graph_controller)
        self.parameters_controller = ParametersController(self.screen,
                                                          self.graph_controller,
                                                          self.file_explorer_controller,
                                                          self.simulation_controller,
                                                          csv_service)

    def handle_actions(self, event) -> None:
        if not self.file_explorer_controller.is_file_explorer_opened():
            self.parameters_controller.handle_events(event)
            self.graph_controller.handle_event(event)
        self.file_explorer_controller.handle_event(event)

    def draw(self) -> None:
        '''
        Cette méthode dessine tous les paramètres et la vue de graph.
        '''
        self.parameters_controller.draw_parameters()
        self.graph_controller.update()
        self.simulation_controller.draw_simulation()
        if self.file_explorer_controller.is_file_explorer_opened():
            self.file_explorer_controller.draw_file_explorer()
