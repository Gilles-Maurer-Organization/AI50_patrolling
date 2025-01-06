import numpy as np
import random as rd

from models.Graph import Graph
from services.algorithms.IAlgorithm import IAlgorithm

class NaiveAlgorithmRuntime(IAlgorithm):
    """
    This class implements the real time Naive Algorithm

    Attributes:
        nb_agents : The number of agents
        graph_object : the object of the Graph Class.

    """

    def __init__(
        self, 
        nb_agents: int,
        graph_object: Graph
    ) -> None:

        self.distance_matrix = np.array(graph_object.get_complete_adjacency_matrix())
        self.nb_nodes = np.array(graph_object.get_complete_adjacency_matrix()).shape[0]
        self.nb_agents = nb_agents
        self.graph = graph_object
        self.path = []
        self.paths = [None] * nb_agents 
        self.positions = [0] * nb_agents  # Actual position of each Agent
        self.targets = [None] * nb_agents  # Next node of each agent
    

    def find_next_node(self, agent_id: int) -> int:
        """
        Find the next Node that the agent will move to 

        Attributes:
            agent_id : The agent to move

        Returns:
            nearest_node : The nearest node with the most idleness
        """

        current_node = self.positions[agent_id]
        min_distance = float('inf')
        nearest_node = None
        max_idleness = -1  # Keep track of the highest idleness

        # Search the node non visited (and not reserved) with the highest idleness
        for i in range(self.nb_nodes):
            if i not in self.targets and i not in self.positions:  # Avoid nodes already visited and reserved as targets
                distance = self.distance_matrix[current_node][i]
                idleness = self.graph.nodes[i].idleness
                if idleness > max_idleness:
                    nearest_node = i
                    min_distance = distance
                    max_idleness = self.graph.nodes[i].idleness
                elif idleness == max_idleness:
                    # If two nodes have the same highest idleness, choose the one with the shorter distance
                    if distance < min_distance:
                        nearest_node = i
                        min_distance = distance
                        max_idleness = self.graph.nodes[i].idleness
        return nearest_node

    def update_target(self, agent_id: int) -> None:
        """
        Update the target node for the agent to move

        Attributes:
            agent_id : The agent to move

        """
        if self.targets[agent_id] is None:
            # Recompute the next node if the agent don't have a target
            # or the target is already a target
            next_node = self.find_next_node(agent_id)
            self.targets[agent_id] = next_node


    def resolve_conflicts(self) -> None:
        """
        Resolve any conflicts between the targeted nodes of each agents

        """

        # If more than one agent focus the same node, resolve the conflicts by priority of index
        target_count = {}
        for target in self.targets:
            if target is not None:
                if target not in target_count:
                    target_count[target] = 0
                target_count[target] += 1
        
        for target, count in target_count.items():
            if count > 1:
                # If more than one agent focus the same node, force the other agents to recompute
                conflicted_agents = [i for i in range(self.nb_agents) if self.targets[i] == target]
                # The first agent keep the target, the other recompute
                for i in conflicted_agents[1:]:
                    self.targets[i] = None
                    self.update_target(i)

    def first_step(self, agent_id: int, node_start : int) -> None:
        """
        Make a step for the agent to move

        Attributes:
            agent_id : The agent to move

        """
        # Initialize all variables
        self.positions[agent_id] = node_start

        # Update the targets of each agents
        self.update_target(agent_id)
        
        # Resolve conflicts
        self.resolve_conflicts()

        self.paths[agent_id] = [self.positions[agent_id],self.targets[agent_id]]

    def step(self, agent_id: int, node_start : int) -> None:
        """
        Make a step for the agent to move

        Attributes:
            agent_id : The agent to move

        """
        # Initialize all variables
        self.positions[agent_id] = node_start
        target_node = self.targets[agent_id]

        if ((node_start == target_node) or (self.graph.nodes[target_node].idleness == 0)):
            self.targets[agent_id] = None

            # Update the targets of each agents
            self.update_target(agent_id)
        
            # Resolve conflicts
            self.resolve_conflicts()
        
        self.paths[agent_id] = [self.positions[agent_id],self.targets[agent_id]]

    def launch(self) -> list[list[int]]:
        """
        Launches the whole Algorithm.

        Returns:
            paths : The Array with the path of each agents
        """
        
        for agent_id in range(self.nb_agents):
            self.first_step(agent_id,rd.randint(0,self.nb_nodes-1))

        return self.paths
    
    def update(self, agent_id: int, start_node: int) -> list[int]:
        """
        Update the path of the agent

        Attributes:
            agent_id : The agent to move
            start_node : the node the agent will start

        Returns:
            agent_path : The path of the selected agent
        """
        
        self.step(agent_id,start_node)

        agent_path = self.paths[agent_id]

        return agent_path