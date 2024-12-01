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
from matplotlib.animation import FuncAnimation

class AntColony:
    """
    This class implements the Ant Colony Optimization (ACO) algorithm for solving pathfinding and optimization problems.

    Attributes:
    ------------
    evaporation_rate : float
        The rate at which pheromones evaporate from the paths, a value between 0 and 1.
    alpha_parameter : float
        Controls the influence of pheromone levels on the decision-making process of the ants.
    beta_parameter : float
        Controls the influence of the distance (or cost) on the decision-making process of the ants.
    nb_ants : int
        The number of ants participating in each iteration of the algorithm.
    nb_iterations : int
        The number of iterations over which the algorithm will run.

    Methods:
    --------
    get_length_path(ants_path):
        Calculates the total distance traveled by each ant for its path.
        
    get_pheromone_matrix(pheromone_matrix, ants_path):
        Updates and returns the pheromone matrix after each ant has completed its path, considering pheromone evaporation.
        
    get_probability(pheromone_matrix):
        Calculates and returns the probability matrix for each ant to move from one node to another based on pheromone levels and cost.
        
    roulette_wheel(probability, current_node, visited):
        Simulates the roulette wheel selection to determine the next node an ant will move to, based on the probability matrix.
        
    launch(node_agent):
        Runs the ant colony optimization algorithm and returns the best path based on the final pheromone matrix.
        
    get_best_path(pheromone_matrix, current_node):
        Returns the path with the highest pheromone levels by following the most popular routes as determined by the ants.
    """
    
    def __init__(self, evaporation_rate, alpha_parameter, beta_parameter, nb_agents, nb_colony, nb_iterations, Q, cost_matrix):
            self.evaporation_rate = evaporation_rate
            self.alpha_parameter = alpha_parameter
            self.beta_parameter = beta_parameter
            self.nb_ants = nb_agents
            self.nb_colony = nb_colony
            self.nb_iterations = nb_iterations
            self.Q = Q
            self.cost_matrix = cost_matrix

    def get_length_path(self, ants_path):
        """
        Calculate the total length of paths taken by all ants.
        This method computes the total distance traveled by each ant based on their respective paths.
        The paths are assumed to be cyclic, meaning the last node in the path is connected back to the first node.
        Args:
            ants_path (list of list of int): A list where each element is a list representing the path taken by an ant.
                                             Each path is a list of node indices.
        Returns:
            float: The sum of the distances traveled by all ants.
        """
        
        # Initialize the distance matrix
        distance = np.zeros(len(ants_path))

        
        # For each ant
        for k_ant, ant_path in enumerate(ants_path):
            # For each node, add distance from the node to next node to the total distance that the ant travel
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
        ants_path is set like : np.array([[0,1,2,,..., 3],[0,2,1, ..., 3], ...]) this mean the first ant go from node 0 to 1 then 1 to 2, etc.
        """
        # Mathematical model to represent phemone level on a graph
        # Initialization
        nb_node = len(self.cost_matrix)

        # Creating delta_t_pheromone_matrix
        delta_t_pheromone_matrix = np.zeros((self.nb_colony, self.nb_ants, nb_node, nb_node), dtype=float)
        for l in range(self.nb_ants):
            for k in range(self.nb_ants):
                np.fill_diagonal(delta_t_pheromone_matrix[l][k], 0)

        # Populate travel_matrix based on ants_path
        for k_colony, ants_path in enumerate(globl_ants_path):
            length_path = self.get_length_path(ants_path)

            for k_ant, ant_path in enumerate(ants_path):
                mask = np.zeros((nb_node, nb_node), dtype=bool)
                # Create a list of pairs (i_nodes, j_nodes) for each node in the ant's path
                i_nodes = np.array(ant_path[:-1])
                j_nodes = np.array(ant_path[1:])
                
                # Mark the nodes the ant travels
                mask[i_nodes, j_nodes] = True

                # The matrix is symetrix, if an ant have passed trouth i to j, that mean it had passed throu j to i
                mask[j_nodes, i_nodes] = True

                # Connect the last node to the first node to handle the loop
                mask[ant_path[-1], ant_path[0]] = True
                # Symetrie
                mask[ant_path[0],  ant_path[-1]] = True

                # Set delta values where the ant travels using boolean masking, usiing Q
                delta_t_pheromone_matrix[k_colony][k_ant][mask] += self.Q / length_path


        # Sum of delta_pheromone_matrix for each ant, without evaporation np.sum, what come before is the evaporation term
        pheromone_matrix = (1 - self.evaporation_rate)*pheromone_matrix + np.sum(delta_t_pheromone_matrix, axis=(0, 1))

        # When evaporation_rate = 0 then it will add the delta pheromone to the old one. When = 1 the old pheromone_matrix is completly evaporated
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
        Get a random number and base on the probability matrix and the node where the ant is. Return from this random roulette wich node did the ant will go next.
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
        next_node_indices = np.nonzero(cumulative_sum >= random_number)[0] # [0] because np.nonzero is a tuple, [0] allows direct retrieval of the array of indices
        if len(next_node_indices) == 0:
            raise IndexError("No valid next node found, check the probability matrix.")
        # Return the first value of next_node_indices bacause it is the next_node chosen based of the random_number and cumulative_sum
        next_node = next_node_indices[0]

        return next_node, prob

    def get_start_nodes(self): 
        # Heuristique to find first node
        nb_nodes = self.cost_matrix.shape[0]

        start_nodes = []
        # List of nodes where an agent can start, IE : 2 agents can't spawn in the same node and an agent can't spaw
        autorize_nodes = [i for i in range(nb_nodes)]

        # Create a random generator
        rng = np.random.default_rng()

        for _ in range(self.nb_ants):
            # Heuristique = random
            random_node = autorize_nodes[rng.integers(len(autorize_nodes))]
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
                next_node, prob_matrix = self.roulette_wheel(global_pheromone_matrix, current_node, tabou_list)
                
                current_nodes[ant] = next_node
                
                ants_path[ant].append(next_node)
                
                tabou_list.append(next_node)

                # If list taboo complete then no more movement possible
                if (len(tabou_list) == nb_nodes):
                    break
        
        # Return the path for this colony
        return ants_path, prob_matrix

        
    def launch(self):
        """
        Launch the ant colony algorithm and return the final best path and path length history.
        
        Parameters:
        - self.cost_matrix: matrix of costs between nodes.
        
        Returns:
        - best_path: the best path found.
        - path_length_history: a list of lists where each inner list contains the total path length for each colony in each iteration.
        """
        # Get the number of nodes
        nb_nodes = self.cost_matrix.shape[0]

        # If more agents than nodes then return error
        if nb_nodes <= self.nb_ants:
            raise IndexError("More agents than nodes in the graph.")

        # Pheromone matrix initialization
        global_pheromone_matrix = np.ones((nb_nodes, nb_nodes))

        # Set the diagonal of the pheromone matrix to 0
        np.fill_diagonal(global_pheromone_matrix, 0)

        # Initialize path length history
        path_length_history = []
        probs_history = []
        pheromone_history = []

        first_nodes = self.get_start_nodes()

        # Stop criteria: nb_iterations
        for _ in range(self.nb_iterations):

            global_ants_path = [[] for _ in range(self.nb_colony)]
            iteration_path_lengths = []  # Store path lengths for this iteration

            # For each colony
            for colony in range(self.nb_colony):
                ants_path, prob_history = self.colony_path(nb_nodes, global_pheromone_matrix, first_nodes)
                probs_history.append(prob_history)
                global_ants_path[colony] = ants_path

                path_length = self.get_length_path(global_ants_path[colony])
                iteration_path_lengths.append(path_length)

            # Append the iteration's path lengths to history
            path_length_history.append(iteration_path_lengths)

            # Pheromone matrix updated after all ants have been relocated
            global_pheromone_matrix = self.get_pheromone_matrix(global_pheromone_matrix, global_ants_path)
            pheromone_history.append(global_pheromone_matrix)

            #Check for convergence
            if self.check_convergence(path_length_history):
                break

        # Get the best path after all iterations
        best_path = self.get_best_path(global_ants_path)
        return best_path, path_length_history, probs_history, pheromone_history

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
    

# Visualisation
def visualize_probability_evolution(probability_matrices, interval=100):
    """
    Visualize the evolution of the probability matrix as an animation.
    
    Arguments:
    - probability_matrices: List of successive probability matrices.
    - interval: Time in milliseconds between each display of the matrix.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap = ax.imshow(probability_matrices[0], cmap="YlGnBu", vmin=0, vmax=1)
    plt.colorbar(heatmap, ax=ax, label="Probability")
    
    def update(step):
        ax.set_title(f"Step {step + 1} - Evolution of the Probability Matrix")
        heatmap.set_data(probability_matrices[step])
        
        # Add values on the heatmap for each cell
        ax.clear()
        ax.imshow(probability_matrices[step], cmap="YlGnBu", vmin=0, vmax=1)
        ax.set_title(f"Step {step + 1} - Evolution of the Probability Matrix")
        
        for i in range(probability_matrices[step].shape[0]):
            for j in range(probability_matrices[step].shape[1]):
                ax.text(j, i, f"{probability_matrices[step][i, j]:.2f}", 
                        ha="center", va="center", color="black", fontsize=8)
        
        ax.set_xlabel("Destination Node")
        ax.set_ylabel("Starting Node")
        
    plt.show()


def visualize_pheromone_evolution(pheromone_matrices, interval=100):
    """
    Visualize the evolution of the pheromone matrix as an animation.
    
    Arguments:
    - pheromone_matrices: List of successive pheromone matrices.
    - interval: Time in milliseconds between each display of the matrix.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap = ax.imshow(pheromone_matrices[0], cmap="YlOrBr", vmin=0, vmax=np.max(pheromone_matrices))
    plt.colorbar(heatmap, ax=ax, label="Pheromone Level")
    
    def update(step):
        ax.clear()  # Clear the axis for each step to avoid text overlap
        ax.imshow(pheromone_matrices[step], cmap="YlOrBr", vmin=0, vmax=np.max(pheromone_matrices))
        ax.set_title(f"Step {step + 1} - Evolution of Pheromones")
        
        # Add values on the heatmap for each cell
        for i in range(pheromone_matrices[step].shape[0]):
            for j in range(pheromone_matrices[step].shape[1]):
                ax.text(j, i, f"{pheromone_matrices[step][i, j]:.2f}", 
                        ha="center", va="center", color="black", fontsize=8)
        
        ax.set_xlabel("Destination Node")
        ax.set_ylabel("Starting Node")
    
    plt.show()



def plot_path_length_history(path_length_history):
    """
    Plot the path length history for each colony over the iterations.
    
    Parameters:
    - path_length_history: list of lists containing path lengths for each colony at each iteration.
    """
    nb_iterations = len(path_length_history)
    nb_colony = len(path_length_history[0]) if nb_iterations > 0 else 0
    
    # Plot path lengths for each colony
    for colony in range(nb_colony):
        lengths = [iteration[colony] for iteration in path_length_history]
        plt.plot(range(nb_iterations), lengths, label=f"Colony {colony + 1}")

    plt.xlabel("Iterations")
    plt.ylabel("Path Length")
    plt.title("Path Length History for Each Colony")
    plt.legend()
    plt.show()


# Exemple of use of the class above
if __name__ == "__main__":

    # Exemple of cost matrix
    cost_matrix = np.array([
        [0, 2, 4, 5, 2, 6, 7, 5, 4, 6, 4, 5, 6, 7, 4],
        [2, 0, 2, 3, 4, 5, 6, 7, 5, 4, 5, 6, 7, 4, 5],
        [4, 2, 0, 2, 6, 4, 5, 6, 7, 5, 6, 7, 4, 5, 6],
        [5, 3, 2, 0, 2, 6, 4, 5, 6, 7, 7, 4, 5, 6, 7],
        [2, 4, 6, 2, 0, 5, 6, 7, 5, 4, 4, 5, 6, 7, 4],
        [6, 5, 4, 6, 5, 0, 2, 4, 5, 2, 5, 6, 7, 4, 5],
        [7, 6, 5, 4, 6, 2, 0, 2, 3, 4, 6, 7, 4, 5, 6],
        [5, 7, 6, 5, 7, 4, 2, 0, 2, 6, 7, 4, 5, 6, 7],
        [4, 5, 7, 6, 5, 5, 3, 2, 0, 2, 4, 5, 6, 7, 4],
        [6, 4, 5, 7, 4, 2, 4, 6, 2, 0, 5, 6, 7, 4, 5],
        [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 0, 2, 4, 5, 2],
        [5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 2, 0, 2, 3, 4],
        [6, 7, 4, 5, 6, 7, 4, 5, 6, 7, 4, 2, 0, 2, 6],
        [7, 4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 3, 2, 0, 2],
        [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 2, 4, 6, 2, 0]
    ])
        

    # Evaporation rate between 0 and 1
    evaporation_rate = 0.7
    alpha_parameter = 1
    beta_parameter = 2
    nb_agents = 3  #Nb agent = nb fourmis
    nb_colony = 3
    nb_iterations = 1000
    Q = 10

    fourmis = AntColony(evaporation_rate, alpha_parameter, beta_parameter, nb_agents,nb_colony, nb_iterations, Q, cost_matrix)

    # launch ant colony algorithm
    final_path, history, prob_history, pheromone_history = fourmis.launch()
    
    print("Best path ", final_path)

    plot_path_length_history(history)