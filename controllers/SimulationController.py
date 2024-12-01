from controllers.GraphController import GraphController
from models.Agent import Agent

class SimulationController:
    def __init__(self, graph_controller: GraphController) -> None:
        self._agents = None
        self._simulation_started = False
        self._graph_controller = graph_controller

    def has_simulation_started(self) -> bool:
        return self._simulation_started
    
    def set_simulation_started(self, started: bool) -> None:
        self._simulation_started = started

    def initialize_agents(self, paths: list[int]) -> None:
        self._agents = [Agent(path, self._graph_controller.graph) for path in paths]
    
    def update_simulation(self):
        for _, agent in enumerate(self._agents):
            agent.move()
    
    def draw_simulation(self) -> None:
        if self._simulation_started:
            self.update_simulation()
            self._graph_controller.draw_simulation(self._agents)