import pygame

from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
from views.SimulationDataView import SimulationDataView
from controllers.IdlenessesController import IdlenessController

class SimulationDataController:

    """
    This class manages everything related to the visualization 
    of Idleness of the simulation.

    Attributes:
        _simulation_data_view: the Simulation section of the View
        _idleness_controller : the Idleness-data controller

    """

    def __init__(self, screen: pygame.Surface, nodes_list) -> None:
        self._simulation_data_view = SimulationDataView(
            screen.subsurface(
                (GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)
            ))
        self._idleness_controller = IdlenessController(nodes_list,self._simulation_data_view)

    def draw_simulation_data(self) -> None:
        """
        Draws the simulation data by updating the idleness's values
        """
        self._simulation_data_view.draw()
        self._idleness_controller.draw_idlenesses()
