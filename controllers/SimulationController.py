import pygame

from controllers.SimulationDataController import SimulationDataController
from controllers.GraphController import GraphController
from models.Agent import Agent
from models.IdlenessData import IdlenessData
from models.Node import Node
from services import CSVService
from services.CSVService import export_idleness_data


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
    def __init__(self, graph_controller: GraphController, simulation_data_controller: SimulationDataController) -> None:
        self._agents = None
        self._simulation_started = False
        self._graph_controller = graph_controller
        self._start_time = None
        self._simulation_data_controller = simulation_data_controller
        self._idleness_data = IdlenessData()

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

        # Start exporting idleness data
        if started:
            self.start_idleness_export(graph_number=1)

    def initialize_agents(self, paths: list[list[int]]) -> None:
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
    
    def _are_agents_on_node(self, node: Node, agents_not_on_nodes: set[Agent]) -> bool:
        """
        For each node verify if an agent is on it, and if so put the idleness at 0
        """
        margin: int = 2
        for agent in list(agents_not_on_nodes):
            if abs(agent.x - node.x) <= margin and abs(agent.y - node.y) <= margin:
                agents_not_on_nodes.remove(agent)
                return True
        
        return False
        
    def _update_simulation(self) -> None:
        """
        Updates the simulation by moving each agent along its path.
        """
        for _, agent in enumerate(self._agents):
            agent.move()

    def _update_nodes_idlenesses(self) -> None:
        """
        Updates the idleness of each node.
        """
        elapsed_time = pygame.time.get_ticks() - self._start_time

        agents_not_on_nodes = set(self._agents)
                
        for node in self._graph_controller.graph.nodes:
            if self._are_agents_on_node(node, agents_not_on_nodes):
                node.idleness = 0
            else:
                if elapsed_time >= 1000:
                    node.idleness += 1
        
        if elapsed_time >= 1000:
            self._start_time = pygame.time.get_ticks()

        # Update IdlenessData after recalculating node idleness
        self._idleness_data.update_idleness(self._graph_controller.graph.nodes)
            
    def draw_simulation(self) -> None:
        """
        Draws the simulation by updating agent positions and rendering
        them on the graph.
        """
        if self._simulation_started:
            self._update_simulation()
            self._update_nodes_idlenesses()
            self._graph_controller.draw_simulation(self._agents)

    def start_idleness_export(self, graph_number: int):
        """
        Starts exporting idleness data every 10 seconds.
        """

        def idleness_data_provider():
            return self._idleness_data.get_idleness_data()

        export_idleness_data(graph_number, idleness_data_provider, interval=10)
