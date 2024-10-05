import numpy as np


def get_length_path(ants_path, cost_matrix):
    """
    Return the distance that each ant of ants_path travel in total for it path
    
    >>> get_length_path(np.array([[0,1,2], [0,2,1]]), np.array([[0,5,1],[1,0,3],[2,3,0]]))
    np.array([10., 5.])
    """

    # Initialize the distance matrix
    distance = np.zeros(len(ants_path))
    
    # For each ant
    for k_ant, ant_path in enumerate(ants_path):
        # For each node, add distance from the node to next node to the total distance that the ant travel
        for k_node, node in enumerate(ant_path):
            # We considerate that it is a loop, so the last node is connected to the first one
            next_node = ants_path[k_ant, k_node +1] if k_node != (len(cost_matrix) - 1) else 0
            distance[k_ant] += cost_matrix[node][next_node]
    
    # Return the distance
    return distance

def get_pheromone_matrix(cost_matrix, pheromone_matrix, ants_path, evaporation_rate):
    """
    Return the new pheromone matrix after the passage of each ant.
    
    The evaporation rate can be set between 0 and 1.
    ants_path is set like : np.array([[0,1,2,,..., 3],[0,2,1, ..., 3], ...]) this mean the first ant go from node 0 to 1 then 1 to 2, etc.
    """
    # Mathematical model to represent phemone level on a graph

    # Initialization
    length_path = get_length_path(ants_path, cost_matrix)
    
    nb_ants = len(ants_path)
    nb_node = len(cost_matrix)

    delta_t_pheromone_matrix = np.zeros((nb_ants, nb_node, nb_node), dtype=float)
    
    travel_matrix = np.zeros((nb_ants, nb_node, nb_node), dtype=bool)

    # Populate travel_matrix based on ants_path
    for k_ant, ant_path in enumerate(ants_path):
        # Create a list of pairs (i_nodes, j_nodes) for each node in the ant's path
        i_nodes = np.array(ant_path[:-1])
        j_nodes = np.array(ant_path[1:])
        
        # Mark the nodes the ant travels
        travel_matrix[k_ant, i_nodes, j_nodes] = True

        # The matrix is symetrix, if an ant have passed trouth i to j, that mean it had passed throu j to i
        travel_matrix[k_ant, j_nodes, i_nodes] = True

        # Connect the last node to the first node to handle the loop
        travel_matrix[k_ant, ant_path[-1], ant_path[0]] = True
        # Symetrie
        travel_matrix[k_ant, ant_path[0],  ant_path[-1]] = True

    # Use a vectorized operation to calculate delta pheromone
    # Iterate over each ant
    for k_ant in range(nb_ants):
        # Get the travel matrix for the kth ant
        mask = travel_matrix[k_ant]

        # Set delta values where the ant travels using boolean masking
        delta_t_pheromone_matrix[k_ant][mask] = 1 / length_path[k_ant]


    # Sum of delta_pheromone_matrix for each ant, without evaporation np.sum, what come before is the evaporation term
    pheromone_matrix = (1 - evaporation_rate)*pheromone_matrix + np.sum(delta_t_pheromone_matrix, axis=0)

    # When evaporation_rate = 0 then it will add the delta pheromone to the old one. When = 1 the old pheromone_matrix is completly evaporated

    return pheromone_matrix


def get_probability(cost_matrix, pheromone_matrix, alpha_parameter, beta_parameter):
    """
    Return a matrix that represent the probability that an ant go from i to j

    Exemple of an output:
    [[0.         0.38709677 0.12903226 0.48387097]
    [0.34782609 0.         0.43478261 0.2173913 ]
    [0.05063291 0.18987342 0.         0.75949367]
    [0.18181818 0.09090909 0.72727273 0.        ]]


    this mean that for the given input, the probability for an ant to go from node 0 to 1 is  0.38709677. From 1 to 0 is 0.34782609. From 1 to 2 is 0.43478261 etc.
    """

    # Calculer la composante de phéromone élevée à la puissance alpha
    pheromone_component = pheromone_matrix ** alpha_parameter # Represent the pheromone level

    # = 1 / cost_matrix si cost_matrix != 0, 0 sinon
    # Utiliser np.errstate pour ignorer les warnings de division par zéro
    with np.errstate(divide='ignore', invalid='ignore'):
        reverse_cost_matrix = np.where(cost_matrix != 0, 1 / cost_matrix, 0)

    # Assurer que length_path est un tableau 2D compatible avec pheromone_matrix
    length_component = reverse_cost_matrix ** beta_parameter # Represent the quality of the i j node on the graph  
    
    # 1 / by the cost because we are intrested in the shortest path

    # With alpha and beta we can increase or decrease the impact of the pheromone and the cost in the process of decision making

    # Calculer la matrice de probabilité
    nominateur = pheromone_component * length_component
    
    # Calculer la matrice de probabilité
    probability_matrix = nominateur / np.sum(nominateur, axis=1, keepdims=True)
    
    return probability_matrix

def roulette_wheel(probability, current_node, visited):
    """
    Get a random number and base on the probability matrix and the node where the ant is. Return from this random roulette wich node did the ant will go next.
    >>> roulette_wheel(np.array([[0,0.5,0.5],[1,0,0], [0.5,0.5,0]]), 1, { })
    0
    >>> roulette_wheel(np.array([[0,0.5,0.5],[1,0,0], [0.5,0.5,0]]), 1, {0})
    2
    """
    # Remove the probability of the current node and visited nodes
    prob = np.copy(probability[current_node])
    prob[list(visited)] = 0
    
    # Normalize the probabilities
    prob /= np.sum(prob)
    
    # Calculate the cumulative sum of the probabilities
    cumulative_sum = np.cumsum(prob)
    
    # Generate a random number
    random_number = np.random.rand()
    
    # Find the next node based on the random number
    next_node = np.where(cumulative_sum >= random_number)[0][0]

    return next_node


       
def lunch(cost_matrix, evaporation_rate, alpha_parameter, beta_parameter, nb_ants, nb_iterations): 
    """
    lunch the ant colony algotirhm. It return the final pheromone matrix.
    
    cost_matrix: cost matrix between nodes.
    evaporation_rate: pheromone evaporation rate (between 0 and 1).
    alpha_parameter: control parameter for pheromone influence.
    beta_parameter: control parameter for distance influence.
    nb_ants: number of ants per iteration.
    nb_iterations: total number of iterations.
    """

    # Pheromone matrix initialization
    nb_nodes = cost_matrix.shape[0]
    pheromone_matrix = np.ones((nb_nodes, nb_nodes))

    # Set the diagonal of the pheromone matrix to 0
    np.fill_diagonal(pheromone_matrix, 0)

    # Stop criteria: nb_iterations
    for _ in range(nb_iterations):
        # Each ant builds a path
        ants_path = np.zeros((nb_ants, nb_nodes), dtype=int)

        for ant in range(nb_ants):
            # Choose a random starting node for each ant
            start_node = np.random.randint(nb_nodes)
            visited = set([start_node]) # Nodes already visited
            ants_path[ant, 0] = start_node

            # Build a complete path for each ant
            for step in range(1, nb_nodes):
                current_node = ants_path[ant, step - 1]

                # Get probabilities to go to other nodes
                prob_matrix = get_probability(cost_matrix, pheromone_matrix, alpha_parameter, beta_parameter)

                # Choose the next node based on the roulette wheel
                next_node = roulette_wheel(prob_matrix, current_node, visited)

                ants_path[ant, step] = next_node
                visited.add(next_node)

        # Pheromone matrix updated after all ants have been relocated
        pheromone_matrix = get_pheromone_matrix(cost_matrix, pheromone_matrix, ants_path, evaporation_rate)

    return pheromone_matrix


def get_best_path(pheromone_matrix, current_node):
    """
    Returns the path chosen based on the maximum pheromones on the nodes.
    """

    nb_nodes = pheromone_matrix.shape[0]
    visited = set()
    path = [current_node]

    # Choose paths based on maximum pheromones until all node are visited
    while len(visited) < nb_nodes:
        visited.add(current_node)

        # Get the pheromones of outgoing paths from the current node
        pheromones = pheromone_matrix[current_node]

        # Hide nodes already visited
        pheromones[list(visited)] = -1   # Impossible value to exclude nodes already visited

        # Find the next node with the maximum number of pheromones
        next_node = np.argmax(pheromones)
        path.append(next_node)
        current_node = next_node

    return path

if __name__ == "__main__":
    # Exemple of cost matrix
    #cost_matrix = np.array([
    #    [0, 5, 15, 4],
    #    [5, 0, 50, 8],
    #    [15, 50, 0, 1],
    #    [4, 8, 1, 0]
    #])

    # Exemple plus complexe
    cost_matrix = np.array([[ 0,  8,  7,  5, 19, 13, 11,  2,  7, 19],
                            [ 8,  0,  4,  3,  7,  3,  7, 20, 17,  3],
                            [ 7,  4,  0,  1, 14,  5,  8,  2,  3, 20],
                            [ 5,  3,  1,  0,  2,  9,  9, 11, 16, 18],
                            [19,  7, 14,  2,  0,  7, 18,  2,  6, 11],
                            [13,  3,  5,  9,  7,  0, 20,  3, 19, 14],
                            [11,  7,  8,  9, 18, 20,  0, 16,  5,  6],
                            [ 2, 20,  2, 11,  2,  3, 16,  0,  4,  6],
                            [ 7, 17,  3, 16,  6, 19,  5,  4,  0, 10],
                            [19,  3, 20, 18, 11, 14,  6,  6, 10,  0]])


    # Evaporation rate between 0 and 1
    # TODO: Erreur lorsque evaporation rate = 1. Prob mis a 0 et roulette wheel donne l'erreur : IndexError: index 0 is out of bounds for axis 0 with size 0
    # TODO: Mettre sous forme de classe
    evaporation_rate = 0.5
    alpha_parameter = 1
    beta_parameter = 2
    nb_ants = 10  # Nombre de fourmis par itération
    nb_iterations = 100  # Nombre total d'itérations

    # Consider we are at the node 0
    current_node = 0

    # Lunch ant colony algorithm
    final_pheromone_matrix = lunch(cost_matrix, evaporation_rate, alpha_parameter, beta_parameter, nb_ants, nb_iterations)
    
    print("Final pheromone matrix:\n", final_pheromone_matrix)
    print("Best path:\n", get_best_path(final_pheromone_matrix, current_node))