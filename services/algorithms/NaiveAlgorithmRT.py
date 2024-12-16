import numpy as np
import random as rd

from models.Graph import Graph
from services.algorithms.IAlgorithm import IAlgorithm

class NaiveAlgorithmRT(IAlgorithm):
    """
    This class implements the real time Naive Algorithm

    Attributes:
        nb_agents : The number of agents
        distance_matrix : the "complete_adjacency_matrix" attribute from the Graph Class.

    """

    def __init__(
        self, 
        nb_agents: int,
        graph_object: Graph
    ) -> None:

        self.distance_matrix = np.array(graph_object.get_complete_adjacency_matrix())
        self.nb_nodes = np.array(graph_object.get_complete_adjacency_matrix()).shape[0]
        self.nb_agents = nb_agents
        self.positions = [0] * nb_agents  # Position actuelle de chaque agent (commencent au nœud 0)
        self.targets = [None] * nb_agents  # Prochains nœuds cibles pour chaque agent
    
    def find_next_node(self, agent_id: int) -> int:
        """
        Find the next Node that the agent will move to 

        Attributes:
            agent_id : The agent to move

        Returns:
            nearest_node : The nearest node and with the most idleness
        """

        current_node = self.positions[agent_id]
        min_distance = float('inf')
        nearest_node = None
        max_oisivete = -1  # Pour garder trace de l'oisiveté maximale en cas d'égalité de distance

        # Rechercher le nœud non visité (et non réservé) avec la plus grande oisiveté
        for i in range(self.nb_nodes):
            if not self.visited[i] and i not in self.targets:  # Éviter les nœuds déjà visités ou réservés
                distance = self.distance_matrix[current_node][i]
                if distance < min_distance:
                    nearest_node = i
                    min_distance = distance
                    max_oisivete = self.oisivete[i]
                elif distance == min_distance:
                    # Si deux nœuds ont la même distance, choisir celui avec la plus grande oisiveté
                    if self.oisivete[i] > max_oisivete:
                        nearest_node = i
                        max_oisivete = self.oisivete[i]
        
        return nearest_node

    def update_targets(self,agent_id: int) -> None:
        """
        Update the target node for the agent to move

        Attributes:
            agent_id : The agent to move

        """
        if self.targets[agent_id] is None or self.visited[self.targets[agent_id]]:
            # Recalculer le prochain nœud uniquement si l'agent n'a pas encore de cible ou que sa cible est déjà visitée
            next_node = self.find_next_node(agent_id)
            self.targets[agent_id] = next_node


    def resolve_conflicts(self) -> None:
        """
        Resolve any conflicts between the targeted nodes of each agents

        """

        # Si plusieurs agents ciblent le même nœud, résoudre le conflit par priorité d'index d'agent
        target_count = {}
        for target in self.targets:
            if target is not None:
                if target not in target_count:
                    target_count[target] = 0
                target_count[target] += 1
        
        for target, count in target_count.items():
            if count > 1:
                # Si plusieurs agents ciblent le même nœud, forcer les autres agents à recalculer
                conflicted_agents = [i for i in range(self.nb_agents) if self.targets[i] == target]
                # Le premier agent garde la cible, les autres doivent recalculer
                for i in conflicted_agents[1:]:
                    self.targets[i] = None

    def step(self,agent_id: int) -> None:
        """
        Make a step for the agent to move

        Attributes:
            agent_id : The agent to move

        """

        # Mise à jour des cibles pour chaque agent
        self.update_targets(agent_id)
        
        # Résoudre les conflits de cibles
        self.resolve_conflicts()

        for agent_id in range(self.nb_agents):
            target = self.targets[agent_id]
            if target is not None:
                # Déplacer l'agent vers le nœud cible
                self.positions[agent_id] = target

    def launch(self):
        """
        Launches the whole Algorithm.
            
        """
        while True:
            for agent_id in range(self.nb_agents):
                self.step(agent_id)