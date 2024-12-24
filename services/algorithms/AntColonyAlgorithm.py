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
        graph: Graph,
        active_plot : bool = True
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
        
        # Normaliser la matrice des couts
        cost_matrix = np.array(graph.get_complete_adjacency_matrix())
        min_cost = np.min(cost_matrix[np.nonzero(cost_matrix)])
        cost_matrix = cost_matrix / min_cost
        self.cost_matrix : np.ndarray  = cost_matrix
        self.active_plot = active_plot
        
        self._list_nodes = np.zeros((len(graph.nodes), 2)) 
        for i in range(len(graph.nodes)): 
            self._list_nodes[i] = np.array([graph.nodes[i].x, graph.nodes[i].y])
        
        self.best_ever_colony_length = float('inf')
        self.graph = graph

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
        delta_t_pheromone_matrix = np.zeros((nb_node, nb_node), dtype=float)
 
        # Initialize variables to track the best colony and its path length
        best_colony_index = None
        best_colony_length = float('inf')

        # Populate travel_matrix based on ants_path
        for k_colony, ants_path in enumerate(globl_ants_path):
            len_path = self.get_length_path(ants_path)

            # Update the best colony if the current one has a shorter path
            if len_path < best_colony_length:
                best_colony_length = len_path
                best_colony_index = k_colony

        for _, ant_path in enumerate(globl_ants_path[best_colony_index]):            
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
            delta_t_pheromone_matrix[mask] += (self.pheromone_quantity / best_colony_length)

        # Sum of delta_pheromone_matrix for each ant, without evaporation np.sum, 
        # what come before is the evaporation term
        pheromone_matrix = (1 - self.evaporation_rate)*pheromone_matrix + delta_t_pheromone_matrix

        # When evaporation_rate = 0 then it will add the delta pheromone to the old one. 
        # When = 1 the old pheromone_matrix is completly evaporated
        return pheromone_matrix

    def get_probability(self, pheromone_matrix, current_node, visited):
        """
        Return a probability vector representing the probability that an ant at the current node 
        moves to each possible next node, while ignoring already visited nodes.
        """
        
        # Prendre uniquement la ligne correspondant au current_node pour la composante phéromonale
        pheromone_component = (pheromone_matrix[current_node]) ** self.alpha_parameter

        # Ajout d'un epsilon pour éviter les zéros dans la matrice des phéromones
        epsilon = 1e-6
        pheromone_component = np.where(pheromone_component == 0, epsilon, pheromone_component)
        
        # Mise à zéro de la diagonale (aucune boucle)
        pheromone_component[current_node] = 0
        
        # Mise à zéro des nœuds déjà visités
        pheromone_component[np.array(list(visited))] = 0

        # Set the nodes in visited to 0 to exclude them from normalization
        cost_matrix = self.cost_matrix[current_node].copy()
        cost_matrix[np.array(list(visited))] = 0

        # Calcul de la composante des coûts inversés élevée à la puissance beta, uniquement pour la ligne current_node
        with np.errstate(divide='ignore', invalid='ignore'):
            reverse_cost_matrix = np.where(cost_matrix != 0, (1 / cost_matrix) ** self.beta_parameter, 0)

        # Calcul du numérateur des probabilités
        probability_vector = pheromone_component * reverse_cost_matrix

        # Normalisation pour obtenir une probabilité valide
        total = np.sum(probability_vector)
        if total > 0:
            probability_vector /= total
        else:
            # Si la somme est nulle, il peut y avoir un problème avec les matrices de phéromones ou de coûts.
            raise ValueError("La somme des probabilités est nulle. Vérifiez les matrices de phéromones et de coûts.")

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

    def get_start_nodes(self) -> list[int]:
        """
        Heuristic to determine the initial starting nodes for ants.

        The method selects the first node based on the highest sum of distances to all other nodes. 
        Subsequent nodes are added iteratively by selecting the farthest possible node from the 
        already selected nodes, with a probability proportional to the inverse of distances.

        Returns:
            list: A list of starting node indices for the ants.
        """
        nb_nodes : int= self.cost_matrix.shape[0]
        start_nodes : list= []

        # Select the first node based on the maximum sum of distances to all other nodes
        first_node = np.argmax(np.sum(self.cost_matrix, axis=1))
        start_nodes.append(first_node)

        # Select subsequent nodes
        for _ in range(self.nb_ants - 1):
            min_distances = []

            # Calculate the minimum distance from each unselected node to the selected nodes
            for node in range(nb_nodes):
                if node in start_nodes:
                    min_distances.append(0)
                else:
                    # Compute the minimum distance between this node and all selected nodes
                    min_distance = min([self.cost_matrix[start_node][node] for start_node in start_nodes])
                    min_distances.append(min_distance)

            # Convert minimum distances to a numpy array
            distances = np.array(min_distances)

            # Normalize probabilities using a transformation of distances
            top_distances = distances ** 8 #power 8
            probabilities = top_distances / top_distances.sum()

            # Select the next node based on probabilities
            next_node = np.random.choice(np.arange(nb_nodes), p=probabilities)

            # Add the selected node to the list of starting nodes
            start_nodes.append(next_node)

        # Return the list of starting nodes
        return start_nodes


    def colony_path(
            self,
            nb_nodes: int,
            global_pheromone_matrix: np.ndarray,
            first_nodes: list[int]
        ) -> tuple[list[list[int]], list[np.ndarray]]:
        """
        Simulates the path construction for a colony of ants in the Ant Colony Optimization algorithm.
        Args:
            nb_nodes (int): The total number of nodes in the graph.
            global_pheromone_matrix (list of list of float): The matrix representing the pheromone levels between nodes.
            first_nodes (list of int): The initial nodes where each ant starts.
        Returns:
            list of list of int: A list containing the paths taken by each ant.
        """

        # Each ant builds a path
        ants_path = [[] for _ in range(self.nb_ants)]

        # Heuristique to find first node
        current_nodes = first_nodes.copy()

        # Initialize tabou list
        tabou_list : list = current_nodes.copy()

        for ant_index in range(self.nb_ants):
            ants_path[ant_index].append(current_nodes[ant_index])

        ant = 0
        # Reapet until list tabou is full IE : All nodes are visited
        while (len(tabou_list) < nb_nodes):
            # Move each ant one at a time to the next node
            # Choose a random starting node for each ant
            current_node = current_nodes[ant]
            
            # Choose the next node based on the roulette wheel
            next_node = self.roulette_wheel(global_pheromone_matrix, current_node, tabou_list)

            path = self.graph.get_shortest_paths()[(current_node, next_node)]
            for node in path:
                if node not in tabou_list:
                    ants_path[ant].append(node)
                    tabou_list.append(node)

            current_nodes[ant] = next_node

            # If list taboo complete then no more movement possible
            if (len(tabou_list) == nb_nodes):
                break

            # Choose next ant by getting the one with the shortest path :
            # Find the ant with the shortest path
            shortest_path_length = float('inf')
            shortest_path_ant = None
            for i, path in enumerate(ants_path):
                if len(path) == 0:
                    continue
                path_length = self.get_length_path([path])
                if path_length < shortest_path_length:
                    shortest_path_length = path_length
                    shortest_path_ant = i

            # If no valid ant found, break the loop
            if shortest_path_ant is None:
                break

            # Set the current ant to the one with the shortest path
            ant = shortest_path_ant
        
        # Return the path for this colony
        return ants_path
    
    def launch(self) -> list[list[int]]:
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
        colony_start_nodes = [self.get_start_nodes() for _ in range(self.nb_colony)]
        
        # Stop criteria: nb_iterations
        for iteration in range(self.nb_iterations):

            global_ants_path = [[] for _ in range(self.nb_colony)]
            iteration_path_lengths = []  # Store path lengths for this iteration

            # For each colony
            for colony in range(self.nb_colony):
                
                ants_path = self.colony_path(nb_nodes, global_pheromone_matrix, colony_start_nodes[colony])
                
                # Echange
                ants_path = self.exchange(ants_path)
                global_ants_path[colony] = ants_path

                path_length = self.get_length_path(global_ants_path[colony])
                iteration_path_lengths.append(path_length)


            # Append the iteration's path lengths to history
            path_length_history.append(iteration_path_lengths)

            # Pheromone matrix updated after all ants have been relocated
            global_pheromone_matrix = self.get_pheromone_matrix(global_pheromone_matrix, global_ants_path)

            #Check for convergence
            if self.has_converged(path_length_history):
                break

            # Initialize variables to track the best colony and its path length
            best_colony_index = None
            best_colony_length = float('inf')
            # Populate travel_matrix based on ants_path
            for k_colony, ants_path in enumerate(global_ants_path):
                len_path = self.get_length_path(ants_path)
                
                # Update the best colony if the current one has a shorter path
                if len_path < best_colony_length:
                    best_colony_length = len_path
                    best_colony_index = k_colony
            
            # Update colony start nodes for the next iteration
            if iteration <= self.nb_colony :
                for colony in range(self.nb_colony):
                    if colony <= iteration:
                        colony_start_nodes[colony] = colony_start_nodes[best_colony_index]
                    else:
                        colony_start_nodes[colony] = self.get_start_nodes()

        # Get the best path after all iterations
        best_path = self.get_best_path(global_ants_path)

        if  self.active_plot:
            self.plot_path_length_history(path_length_history)
            self._plot_path(best_path)
        
        return best_path

    def has_converged(self, path_length_history: list[list[float]], n: int = 10) -> bool:
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

    def exchange(self, ants_path: list[list[int]]) -> list[list[int]]:
        """"
        Exchange nodes between ants if the distance between nodes is too large.
        Args:
            ants_path (list[list[int]]): A list of paths, where each path is a list of
            node indices representing the path of an ant.
        Returns:
            list[list[int]]: The modified list of paths after exchanging nodes between ants.
        """

        #self._plot_path(ants_path)
        for _, ant_path in enumerate(ants_path):
            # Find the node with the largest distance to its next node
            big_distance = 0
            big_node_index = 0
            for k_node, node in enumerate(ant_path):
                next_node = ant_path[k_node + 1] if k_node != (len(ant_path) - 1) else ant_path[0]
                distance = self.cost_matrix[node][next_node]
                if distance > big_distance:
                    big_distance = distance
                    big_node_index = k_node

            # Remove the node with the largest distance from the ant's path
            big_node = ant_path.pop(big_node_index)

            # Find the ant with the closest node to the removed node
            min_distance = float('inf')
            closest_ant_index = 0
            closest_node_index = 0
            for other_ant_index, other_ant_path in enumerate(ants_path):
                for k_node, node in enumerate(other_ant_path):
                    distance = self.cost_matrix[big_node][node]
                    if distance < min_distance:
                        min_distance = distance
                        closest_ant_index = other_ant_index
                        closest_node_index = k_node
            # Insert the removed node into the closest ant's path
            ants_path[closest_ant_index].insert(closest_node_index + 1, big_node)

        return ants_path

    def plot_path_length_history(self, path_length_history: list[list[np.ndarray]]) -> None:
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

    def _plot_path(self, paths: list[list[int]]) -> None:
        """
        Display the paths of agents on a 2D plot. Each agent's path is shown 
        in a different color.

        Args:
            paths (list of list of int): A list of paths, where each path is 
            a list of node indices representing the trajectory of an agent.
        """
        # Liste de couleurs pour différencier les chemins des agents
        path_colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'lime', 'brown']

        # Créer le graphique
        fig, ax = plt.subplots()

        for i, path in enumerate(paths):
            # Récupérer les coordonnées des nœuds dans le chemin
            coordinates = self._list_nodes[path]  # `self._list_nodes` contient les coordonnées des nœuds
            x, y = coordinates[:, 0], coordinates[:, 1]

            # Tracer le chemin avec une couleur différente pour chaque agent
            ax.plot(x, y, color=path_colors[i % len(path_colors)], label=f'Agent {i+1}')
            ax.scatter(x, y, color=path_colors[i % len(path_colors)], s=50)  # Marquer les nœuds du chemin

        # Ajouter des étiquettes et une légende
        ax.set_title('Paths of Agents')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        plt.show()

    def get_best_path(self, global_ants_path: list[list[int]]) -> list[list[int]]:
        """
        Get the best path based on the maximum pheromones on the nodes.

        Args:
            global_ants_path (List[List[int]]): A list of paths taken by all ants in the colony.

        Returns:
            List[int]: The best path chosen based on the maximum pheromones on the nodes.
        """
        # Implementation of the function
        best_len_path = float('inf')
        best_len_path_num = 0
        for num, ants_path in enumerate(global_ants_path):
            len_path = self.get_length_path(ants_path)

            if len_path < best_len_path:
                best_len_path_num = num
                best_len_path = len_path

        return global_ants_path[best_len_path_num]