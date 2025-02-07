import pygame

from controllers.GraphController import GraphController
from models.Agent import Agent
from models.Node import Node
from services.algorithms.IAlgorithm import IAlgorithm
from services.algorithms.NaiveAlgorithmRuntime import NaiveAlgorithmRuntime

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
    def __init__(
        self,
        graph_controller: GraphController
    ) -> None:
        self._agents = None
        self._simulation_started = False
        self._graph_controller = graph_controller
        self._start_time = None
        self._selected_algorithm = None
        self._test_counters = {}

    def has_simulation_started(self) -> bool:
        """
        Checks if the simulation has started.

        Returns:
            bool: True if the simulation has started, False otherwise.
        """
        return self._simulation_started

    def set_simulation_started(self, started: bool) -> None:
        """
        Sets the simulation state to started or stopped, and initializes idleness export.

        Args:
            started (bool): Whether to start or stop the simulation.
            algorithm (str): The name of the algorithm being used.
        """
        self._simulation_started = self._graph_controller.is_in_simulation = started
        if started:
            self._start_time = pygame.time.get_ticks()
        else:
            self._graph_controller.reset_nodes_idleness()

    def set_selected_algorithm(self, selected_algorithm: IAlgorithm) -> None:
        """
        Sets the selected algorithm for the run time Update

        Args:
            started: The selected Algorithm
        """
        self._selected_algorithm = selected_algorithm

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
    
    def are_agents_on_node(self, node: Node) -> tuple[bool, Agent, int]:
        """
        For each node verify if an agent is on it, and if so put the idleness at 0
        """
        margin: int = 2
        for agent_id, agent in enumerate(self._agents):
            if abs(agent.x - node.x) <= margin and abs(agent.y - node.y) <= margin:
                return True,agent,agent_id
        
        return False,None,0
        
    def _update_simulation(self) -> None:
        """
        Updates the simulation by moving each agent along its path.
        """
        for _, agent in enumerate(self._agents):
            agent.move()
            if (not(isinstance(self._selected_algorithm,NaiveAlgorithmRuntime)) and (agent.current_index >= len(agent.path) - 1)):
                agent.reset_path()

    def _update_node_idleness(self) -> None:
        """
        Updates the idleness of each node.
        """
        elapsed_time = pygame.time.get_ticks() - self._start_time

        for node in self._graph_controller.graph.nodes:
            is_agent_on_node, agent, agent_id = self.are_agents_on_node(node)
            if is_agent_on_node:
                # Recompute the path of an agent only in Real Time
                if(isinstance(self._selected_algorithm,NaiveAlgorithmRuntime) & (agent.current_index == 1)):
                    # Update the path
                    new_path: list[int] = self._selected_algorithm.update(agent_id, agent.path[1])

                    # Compute the updated path to match the view 
                    real_paths: list[list[int]] = self._graph_controller.compute_real_paths([new_path])

                    # Keep only the two first elements of the computed path
                    new_agent_path: list[int] = real_paths[0]
                    agent.path = [new_agent_path[0],new_agent_path[1]]

                    agent.reset_path()

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
            self._update_simulation()
            self._update_node_idleness()
            self._graph_controller.draw_simulation(self._agents)

    def start_idleness_export(self, algorithm: str, test_number: int, start_time: float):
        """
        Starts exporting idleness data every 10 seconds with metadata.

        Args:
            algorithm (str): The name of the algorithm being used in the simulation.
            test_number (int): The current test number for this simulation.
            start_time (float): The simulation start time in seconds.
        """

        def idleness_data_provider():
            return self._idleness_data.get_idleness_data()

        self._csv_service.export_idleness_data(
            idleness_data_provider=idleness_data_provider,
            algorithm=algorithm,
            test_number=test_number,
            start_time=start_time,
            interval=10
        )
