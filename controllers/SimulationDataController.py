import pygame

from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
from views.SimulationDataView import SimulationDataView
from controllers.IdlenessesController import IdlenessController

class SimulationDataController:
    def __init__(self, screen: pygame.Surface) -> None:
        self._simulation_data_view = SimulationDataView(
            screen.subsurface(
                (GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)
            ))
        self._idleness_controller = IdlenessController([],self._simulation_data_view)

    def draw_simulation_data(self) -> None:
        self._simulation_data_view.draw()
        self._idleness_controller.draw_idlenesses()
