from controllers.GraphController import GraphController
from models.Agent import Agent

class SimulationController:
    """
    This class manages the logic for running the simulation. 

    It handles the initialization of agents, updates their movements,
    and draws their current states on the graph.

    Attributes:
        _agents (list[Agent]): The list of agents participating in the
            simulation.
        _simulation_started (bool): Indicates whether the simulation is
            currently running.
        _graph_controller (GraphController): The controller managing
            the graph and its visualization.
    """
    def __init__(self, graph_controller: GraphController) -> None:
        self._agents = None
        self._simulation_started = False
        self._graph_controller = graph_controller

    def has_simulation_started(self) -> bool:
        """
        Checks if the simulation has started.

        Returns:
            bool: True if the simulation has started, False otherwise.
        """
        return self._simulation_started
    
    def set_simulation_started(self, started: bool) -> None:
        """
        Sets the simulation state to started or stopped.

        Args:
            started: A boolean indicating whether the simulation should
                start or stop.
        """
        self._simulation_started = started

    def initialize_agents(self, paths: list[int]) -> None:
        """
        Initializes the agents with their respective paths.

        Args:
            paths: A list of integers representing the initial paths
                for each agent.
        """
        self._agents = [Agent(path, self._graph_controller.graph)
                        for path in paths]
    
    def update_simulation(self) -> None:
        """
        Updates the simulation by moving each agent along its path.
        """
        for _, agent in enumerate(self._agents):
            agent.move()
    
    def draw_simulation(self) -> None:
        """
        Draws the simulation by updating agent positions and rendering
        them on the graph.
        """
        if self._simulation_started:
            self.update_simulation()
            self._graph_controller.draw_simulation(self._agents)

# TODO : 
# Place les agents ensuite une boule infini arreter sur ordre de l'utilisateur
# Chaque agent est ce que il est en trqin de se deplacer ou est ce que il est sur un noeud
# Agent.py
# S'il est en train de se faire deplacer sinon regarder prochain dans la liste ou real time