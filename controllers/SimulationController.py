import pygame
from controllers.GraphController import GraphController
from models.Agent import Agent
from models.Node import Node
from views.AgentView import AgentView

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
        self._agents_view = []
        self._simulation_started = False
        self._graph_controller = graph_controller
        self._start_time = None

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
        self._start_time = pygame.time.get_ticks()
        self._graph_controller.is_in_simulation = True

    def initialize_agents(self, paths: list[int]) -> None:
        """
        Initializes the agents with their respective paths.

        Args:
            paths: A list of integers representing the initial paths
                for each agent.
        """
        self._agents = [
            Agent(path, self._graph_controller.graph)
                for path in paths
        ]
    
    def are_agents_on_node(self, node: Node) -> bool:
        """
        For each node verify if an agent is on it, and if so put the idleness at 0
        """
        margin: int = 2
        for _, agent in enumerate(self._agents):
            if abs(agent.x - node.x) <= margin and abs(agent.y - node.y) <= margin:
                return True
        
        return False
        
    def update_simulation(self) -> None:
        """
        Updates the simulation by moving each agent along its path.
        """
        for _, agent in enumerate(self._agents):
            agent.move()

    def update_node_idleness(self) -> None:
        """
        Updates the idleness of each node.
        """
        elapsed_time = pygame.time.get_ticks() - self._start_time
                
        for node in self._graph_controller.graph.nodes:
            if self.are_agents_on_node(node):
                node.idleness = 0
            else:
                if elapsed_time >= 1000:
                    node.idleness += 1
        
        if elapsed_time >= 1000:
            self._start_time = pygame.time.get_ticks()      
            
    def draw_simulation(self) -> None:
        """
        Draws the simulation by updating agent positions and rendering
        them on the graph.
        """
        if self._simulation_started:
            self._popup_start_time = pygame.time.get_ticks()
            self.update_simulation()
            self.update_node_idleness()
            self._graph_controller.draw_simulation(self._agents)