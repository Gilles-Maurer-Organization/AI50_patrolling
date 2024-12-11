import pygame

from views.SimulationDataView import SimulationDataView

class SimulationDataController:
    def __init__(self, screen: pygame.Surface) -> None:
        self._simulation_data_view = SimulationDataView(screen)

    def draw_simulation_data(self) -> None:
        self._simulation_data_view.draw()