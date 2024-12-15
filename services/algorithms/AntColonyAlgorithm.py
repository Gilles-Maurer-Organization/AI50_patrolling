"""
This module implements the Ant Colony Optimization (ACO) algorithm, adapted for the multi-patrolling probleme.

The AntColony class provides an implementation of ACO, a probabilistic technique used to find optimal paths based on the behavior of ants in nature.
It is designed to solve pathfinding and combinatorial optimization problems using a population of artificial 'ants' that explore potential solutions.
The class includes functionalities for pheromone management, probability-based path selection, and iterative optimization.

Usage example:
--------------
To use this module, instantiate the AntColony class with the desired parameters, and call the `launch` method with a cost matrix and starting node.

Example:
    >>> colony = AntColony(evaporation_rate=0.5, alpha_parameter=1, beta_parameter=2, nb_ants=10, nb_iterations=100, Q = 10, self.cost_matrix=self.cost_matrix)
    >>> best_path = colony.launch()
"""

from matplotlib import pyplot as plt
import numpy as np
import time as time
from models.Graph import Graph
from models.TextBox import TextBox
from services.algorithms.IAlgorithm import IAlgorithm

class AntColonyAlgorithm(IAlgorithm):
    """
    AntColonyAlgorithm is an implementation of the Ant Colony Optimization (ACO) algorithm.
    This algorithm is used to find the shortest path in a graph by simulating the behavior of ants
    searching for food. The ants deposit pheromones on the paths they take, and the probability of
    choosing a path increases with the amount of pheromone on that path.
    Attributes:
        evaporation_rate (float): The rate at which pheromones evaporate.
        alpha_parameter (float): The influence of pheromone concentration on path selection.
        beta_parameter (float): The influence of path cost on path selection.
        pheromone_quantity (float): The amount of pheromone deposited by each ant.
        nb_ants (int): The number of ants in the colony.
        nb_colony (int): The number of colonies.
        nb_iterations (int): The number of iterations to run the algorithm.
        cost_matrix (np.ndarray): The matrix representing the cost between nodes.
    Methods:
        __init__(self, parameters: dict[str, TextBox], nb_agents: int, cost_matrix) -> None:
            Initializes the AntColonyAlgorithm with the given parameters.
        get_length_path(self, ants_path) -> float:
            Calculates the total length of paths taken by all ants.
        get_pheromone_matrix(self, pheromone_matrix, globl_ants_path):
            Returns the new pheromone matrix after the passage of each ant.
        get_probability(self, pheromone_matrix, current_node, visited):
            Returns a probability vector representing the probability that an ant at the current node 
        roulette_wheel(self, pheromone_matrix, current_node, visited):
            Returns the next node for an ant based on the roulette wheel selection method.
        get_start_nodes(self):
            Returns the starting nodes for each ant.
        colony_path(self, nb_nodes, global_pheromone_matrix, first_nodes):
            Builds a path for each ant in the colony.
        launch(self):
            Launches the ant colony algorithm and returns the final best path and path length history.
        check_convergence(self, path_length_history, n=10):
            Checks if the algorithm has converged based on the path length history.
        plot_path_length_history(self, path_length_history):
            Plots the path length history for each colony over the iterations.
        get_best_path(self, global_ants_path):
            Returns the best path found by the algorithm.
    """

    def __init__(
        self, 
        parameters: dict[str, TextBox],
        nb_agents: int,
        graph_object: Graph,
        active_plot : bool = False
    ) -> None:
        # Get parameters
        alpha_parameter: float =  float(parameters["Alpha"].text_content)
        beta_parameter: float =  float(parameters["Beta"].text_content)
        pheromone_quantity: float =  float(parameters["Pheromone quantity"].text_content)
        nb_colony: int =  int(parameters["Nb colony"].text_content)
        nb_iterations: int =  int(parameters["Nb iterations"].text_content)
        evaporation_rate: float =  float(parameters["Evaporation rate"].text_content)  

        # Validation of the parameters
        if not (0 < evaporation_rate <= 1):
            raise ValueError("The evaporation rate must be between 0 and 1 (exclusive for 0).")
        if alpha_parameter <= 0:
            raise ValueError("The alpha parameter must be greater than 0.")
        if beta_parameter <= 0:
            raise ValueError("The beta parameter must be greater than 0.")
        if nb_agents <= 0:
            raise ValueError("The number of agents must be greater than 0.")
        if nb_colony <= 0:
            raise ValueError("The number of colonies must be greater than 0.")
        if nb_iterations <= 0:
            raise ValueError("The number of iterations must be greater than 0.")
        if pheromone_quantity <= 0:
            raise ValueError("The pheromone quantity must be greater than 0.")
            
        self.evaporation_rate: float = evaporation_rate
        self.alpha_parameter: float = alpha_parameter
        self.beta_parameter: float = beta_parameter
        self.pheromone_quantity : float = pheromone_quantity
        self.nb_ants : int = nb_agents
        self.nb_colony : int = nb_colony
        self.nb_iterations : int = nb_iterations
        self.cost_matrix : np.ndarray  = np.array(graph_object.get_complete_adjacency_matrix())
        self.active_plot = active_plot

    def get_length_path(self, ants_path) -> float:
        """
        Calculate the total length of paths taken by all ants.
        This method computes the total distance traveled by each ant based on their respective paths.
        The paths are assumed to be cyclic, meaning the last node in the path is connected back to the first node.
        Args:
            ants_path (list of list of int):
                A list where each element is a list representing the path taken by an ant.
                Each path is a list of node indices.
        Returns:
            float: The sum of the distances traveled by all ants.
        """
        
        # Initialize the distance matrix
        distance = np.zeros(len(ants_path))

        
        # For each ant
        for k_ant, ant_path in enumerate(ants_path):
            # For each node, add distance from the node to next node to 
            # the total distance that the ant travel
            for k_node, node in enumerate(ant_path):
                # We considerate that it is a loop, so the last node is connected to the first one
                next_node = ant_path[k_node + 1] if k_node != (len(ant_path) - 1) else ant_path[0]
                distance[k_ant] += self.cost_matrix[node][next_node]
        
        # Return the distance
        return np.sum(distance)

    def get_pheromone_matrix(self, pheromone_matrix, globl_ants_path):
        """
        Return the new pheromone matrix after the passage of each ant.
        
        The evaporation rate can be set between 0 and 1.
        ants_path is set like : np.array([[0,1,2,,..., 3],[0,2,1, ..., 3], ...])
        this mean the first ant go from node 0 to 1 then 1 to 2, etc.
        """
        # Mathematical model to represent phemone level on a graph
        # Initialization
        nb_node = len(self.cost_matrix)

        # Creating delta_t_pheromone_matrix
        delta_t_pheromone_matrix = np.zeros((self.nb_colony, self.nb_ants, nb_node, nb_node), dtype=float)
        for l in range(self.nb_colony):
            for k in range(self.nb_ants):
                np.fill_diagonal(delta_t_pheromone_matrix[l][k], 0)

        # Populate travel_matrix based on ants_path
        for k_colony, ants_path in enumerate(globl_ants_path):
            length_path = self.get_length_path(ants_path)

            for k_ant, ant_path in enumerate(ants_path):
                # If the ant_path contain only 1 node
                # (ie there are as many agents as node or more than half), then we pass
                if len(ant_path) <= 1:
                    break
                mask = np.zeros((nb_node, nb_node), dtype=bool)
                # Create a list of pairs (i_nodes, j_nodes) for each node in the ant's path
                i_nodes = np.array(ant_path[:-1])
                j_nodes = np.array(ant_path[1:])
                
                # Mark the nodes the ant travels
                mask[i_nodes, j_nodes] = True

                # The matrix is symetrix, if an ant have passed trouth i to j,
                # that mean it had passed throu j to i
                mask[j_nodes, i_nodes] = True

                # Connect the last node to the first node to handle the loop
                mask[ant_path[-1], ant_path[0]] = True
                # Symetrie
                mask[ant_path[0],  ant_path[-1]] = True

                # Set delta values where the ant travels using boolean masking, usiing Q
                delta_t_pheromone_matrix[k_colony][k_ant][mask] += self.pheromone_quantity / length_path


        # Sum of delta_pheromone_matrix for each ant, without evaporation np.sum, 
        # what come before is the evaporation term
        pheromone_matrix = (1 - self.evaporation_rate)*pheromone_matrix + np.sum(delta_t_pheromone_matrix, axis=(0, 1))

        # When evaporation_rate = 0 then it will add the delta pheromone to the old one. 
        # When = 1 the old pheromone_matrix is completly evaporated
        return pheromone_matrix


    def get_probability(self, pheromone_matrix, current_node, visited):
        """
        Return a probability vector representing the probability that an ant at the current node 
        moves to each possible next node, while ignoring already visited nodes.
        """
        # Calculation of the pheromone component raised to alpha power
        pheromone_component = pheromone_matrix ** self.alpha_parameter

        # Calculation of the high-cost component at beta power
        with np.errstate(divide='ignore', invalid='ignore'):
            reverse_cost_matrix = np.where(self.cost_matrix != 0, (1 / self.cost_matrix)** self.beta_parameter, 0)
        

        length_component = reverse_cost_matrix
        
        # Calculating the numerator of the probability
        nominateur = pheromone_component * length_component

        # Apply a mask to ignore nodes already visited
        probability_vector = nominateur[current_node].copy()
        probability_vector[visited] = 0  # Exclure les nœuds visités
        
        # Normalization to obtain the probability
        total = np.sum(probability_vector)
        if total > 0:
            probability_vector /= total
        
        # Return the probability vector
        return probability_vector


    def roulette_wheel(self, pheromone_matrix, current_node, visited):
        """
        Get a random number and base on the probability matrix and the node where the ant is. 
        Return from this random roulette wich node did the ant will go next.
        >>> roulette_wheel(np.array([[0,0.5,0.5],[1,0,0], [0.5,0.5,0]]), 1, { })
        0
        >>> roulette_wheel(np.array([[0,0.5,0.5],[1,0,0], [0.5,0.5,0]]), 1, {0})
        2
        """
        
        prob = self.get_probability(pheromone_matrix, current_node, visited)
        
        # Calculate the cumulative sum of the probabilities
        cumulative_sum = np.cumsum(prob)
        
        # Generate a random number
        # Create a default random number generator
        rng = np.random.default_rng()

        # Generate a random number between 0 and 1
        random_number = rng.random()
        
        # Find the next node based on the random number
        # [0] because np.nonzero is a tuple, [0] allows direct retrieval of the array of indices
        next_node_indices = np.nonzero(cumulative_sum >= random_number)[0]
        if len(next_node_indices) == 0:
            raise IndexError("No valid next node found, check the probability matrix.")
        # Return the first value of next_node_indices bacause it 
        # is the next_node chosen based of the random_number and cumulative_sum
        next_node = next_node_indices[0]

        return next_node

    def get_start_nodes(self): 
        # Heuristique to find first node
        nb_nodes = self.cost_matrix.shape[0]

        start_nodes = []
        # List of nodes where an agent can start, IE : 
        # 2 agents can't spawn in the same node and an agent can't spawn
        autorize_nodes = [i for i in range(nb_nodes)]

        # Create a random generator
        rng = np.random.default_rng()

        for _ in range(self.nb_ants):
            if not start_nodes:
                # If no start nodes yet, choose randomly
                random_node = autorize_nodes[rng.integers(len(autorize_nodes))]
            else:
                # Calculate distances from already selected nodes
                distances = np.zeros(len(autorize_nodes))
                for i, node in enumerate(autorize_nodes):
                    distances[i] = np.min([self.cost_matrix[node][start_node] for start_node in start_nodes])
                
                # Choose the node with the maximum minimum distance
                random_node = autorize_nodes[np.argmax(distances)]
            
            start_nodes.append(random_node)
            autorize_nodes.remove(random_node)
        
        # Return first node of each ant
        return start_nodes
    def colony_path(self, nb_nodes, global_pheromone_matrix, first_nodes):
        # Each ant builds a path
        ants_path = [[] for _ in range(self.nb_ants)]

        # Heuristique to find first node
        current_nodes = first_nodes

        # Initialize tabou list
        tabou_list = current_nodes.copy()

        for ant_index in range(self.nb_ants):
            ants_path[ant_index].append(current_nodes[ant_index])

        # Reapet until list tabou is full IE : All nodes are visited
        while (len(tabou_list) < nb_nodes):
            # Move each ant one at a time to the next node
            for ant in range(self.nb_ants):
                # Choose a random starting node for each ant
                current_node = current_nodes[ant]
                
                # Choose the next node based on the roulette wheel
                next_node = self.roulette_wheel(global_pheromone_matrix, current_node, tabou_list)
                
                current_nodes[ant] = next_node
                
                ants_path[ant].append(next_node)
                
                tabou_list.append(next_node)

                # If list taboo complete then no more movement possible
                if (len(tabou_list) == nb_nodes):
                    break
        
        # Return the path for this colony
        return ants_path

        
    def launch(self):
        """
        Launch the ant colony algorithm and return the final best path and path length history.
        
        Parameters:
        - self.cost_matrix: matrix of costs between nodes.
        
        Returns:
        - best_path: the best path found.
        - path_length_history: a list of lists where each inner list 
            contains the total path length for each colony in each iteration.
        """
        # Get the number of nodes
        nb_nodes = self.cost_matrix.shape[0]

        # Pheromone matrix initialization
        global_pheromone_matrix = np.ones((nb_nodes, nb_nodes))

        # Set the diagonal of the pheromone matrix to 0
        np.fill_diagonal(global_pheromone_matrix, 0)

        # Initialize path length history
        path_length_history = []

        first_nodes = self.get_start_nodes()

        # Stop criteria: nb_iterations
        for _ in range(self.nb_iterations):

            global_ants_path = [[] for _ in range(self.nb_colony)]
            iteration_path_lengths = []  # Store path lengths for this iteration

            # For each colony
            for colony in range(self.nb_colony):
                ants_path = self.colony_path(nb_nodes, global_pheromone_matrix, first_nodes)
                global_ants_path[colony] = ants_path

                path_length = self.get_length_path(global_ants_path[colony])
                iteration_path_lengths.append(path_length)

            # Append the iteration's path lengths to history
            path_length_history.append(iteration_path_lengths)

            # Pheromone matrix updated after all ants have been relocated
            global_pheromone_matrix = self.get_pheromone_matrix(global_pheromone_matrix, global_ants_path)

            #Check for convergence
            if self.check_convergence(path_length_history):
                break

        # Get the best path after all iterations
        best_path = self.get_best_path(global_ants_path)

        if  self.active_plot:
            self.plot_path_length_history(path_length_history)
        
        return best_path

    def check_convergence(self, path_length_history, n=10):
        """
        Check if the algorithm has converged based on the path length history.
        
        Parameters:
            path_length_history (list): History of path lengths to check for convergence.
            n (int): Number of recent iterations to consider for convergence.
            
        Returns:
            bool: True if the algorithm has converged, False otherwise.
        """
        if len(path_length_history) < n:
            return False

        # Check if the path lengths have not changed significantly in the last n iterations
        recent_lengths = path_length_history[-n:]  # Get the last n path lengths
        last_lengths = recent_lengths[-1]

        # Verify if all recent path lengths are close to the most recent one
        return all(np.allclose(last_lengths, lengths, atol=1e-2) for lengths in recent_lengths[:-1])

    def plot_path_length_history(self, path_length_history: list[list[np.ndarray]]):
        """
        Plot the path length history for each colony over the iterations.
        
        Parameters:
        - path_length_history: list of lists containing path lengths for each colony at each iteration.
        """
        nb_iterations = len(path_length_history)
        nb_colony = len(path_length_history[0]) if nb_iterations > 0 else 0
        
        # Tracer les longueurs de chemin pour chaque colonie
        for colony in range(nb_colony):
            lengths = [iteration[colony] for iteration in path_length_history]
            plt.plot(range(nb_iterations), lengths, label=f"Colony {colony + 1}")

        plt.xlabel("Iterations")
        plt.ylabel("Path Length")
        plt.title("Path Length History for Each Colony")
        plt.legend()
        plt.show()

    def get_best_path(self, global_ants_path):
        """
        Returns the path chosen based on the maximum pheromones on the nodes.
        """
        best_len_path = float('inf')
        best_len_path_num = 0
        for num, ants_path in enumerate(global_ants_path):
            len_path = self.get_length_path(ants_path)

            if len_path < best_len_path:
                best_len_path_num = num
                best_len_path = len_path

        return global_ants_path[best_len_path_num]