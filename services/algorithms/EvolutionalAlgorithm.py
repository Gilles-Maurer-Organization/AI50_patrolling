import random as rd
import time

from models.Graph import Graph
from models.TextBox import TextBox
from services.algorithms.IAlgorithm import IAlgorithm

import numpy as np


class EvolutionalAlgorithm(IAlgorithm):
    """
    This class implements a regular Genetics Algorithm.

    Attributes:
        nb_generations : The number of generation the Algorithm has to perform.

        nb_agents : The number of agents (defines the size of an individual).

        nb_individuals_in_pop : The number of individuals in the population.

        indicative_paths_population : Contains the "short" version of the pat,
         thus ignoring the case when 2 following nodes in the path don't have a direct link.

        real_paths_population : Contains the "real" path by adding the
        additional nodes between 2 nodes which don't have a direct link

        shortest_way_dict : the "shortest_paths" attribute from the Graph Class.

        distance_matrix : the "complete_adjacency_matrix" attribute from the Graph Class.

        nodes_idx_list : Stores a sorted list of all the nodes contained the Graph.

        number_of_crossing_points : nb of crossing points used in the Algorithm

        crossing_rate :  the crossing rate used in the Algorithm

        mutation_rate : the mutating rate used in the Algorithm
    """

    # The "# NOSONAR" comments you'll see next to the random number generators are used to tell SonarCloud
    # to skip the associated warnings as the random generators are used on purpose.

    def __init__(
            self, 
            parameters : dict[str, TextBox], 
            nb_agents: int ,
            graph_object: Graph
        ) -> None :

        self.nb_generations : int = int(parameters["Number of iterations"].text_content)
        self.nb_agents = nb_agents
        self.nb_individuals_in_pop : int = int(parameters["Number of individuals"].text_content)
        self.indicative_paths_population = []
        self.real_paths_population = []
        self.shortest_way_dict = graph_object.get_shortest_paths()
        self.distance_matrix = graph_object.get_complete_adjacency_matrix()
        self.nodes_idx_list = np.arange(0, len(graph_object.get_complete_adjacency_matrix()))
        self.number_of_crossing_points = 2
        self.crossing_rate = 0.8
        self.mutation_rate = 0.5

    def initial_population_generation(self) -> np.ndarray:
        """
        Generates a random initial population for the Algorithm.
        Also verifies that the generated individual is indeed valid
        thus helps the algorithm for converging faster

        Returns:
            ndarray: the generated indicative population.
        """

        # maximal number of tries allowed
        max_tries = 10

        indicative_population = []

        # For each individual
        for _ in range(self.nb_individuals_in_pop):
            
            #splitting the list of nodes of the Graph
            graph_sublists = self.split_list()

            # while the individual is not covering all nodes, we generate him
            # we generate another one (max 10 tries)
            nb_tries_individual = 0
            while (nb_tries_individual < max_tries):

                individual = []
                # For each gene of the individual (a gene is a path of an agent)
                for _ ,init_path  in zip(range(self.nb_agents),graph_sublists):

                    # we shuffle the initial_path (the sublist)
                    rd.shuffle(init_path) #NOSONAR

                    #adding to the individual
                    individual.append(init_path)
                    
                individual = np.array(individual)

                # verifying of the individual covers all nodes at least once
                if self.are_all_nodes_visited(individual):
                    # Appending the individual to the population if he's OK
                    indicative_population.append(individual)
                    break

                else:
                    # if it's the last attempt, we add the individual (even if he's not valid )
                    nb_tries_individual+=1
                    if nb_tries_individual == max_tries:
                        indicative_population.append(individual)

        # Transforming into np.array for later use
        indicative_population = np.array(indicative_population)

        return indicative_population

    def split_list(self)-> list[list]:
        """
        Splits the list containing all the nodes of the Graph
        into a list of sublists having the same length.

        Returns:
            A list of sublists
        """

        if self.nb_agents <= 0:
            raise ValueError("The number of agents must be greater than 0.")

        # computing the size of the sublists
        base_size = len(self.nodes_idx_list) // self.nb_agents
        extra = len(self.nodes_idx_list) % self.nb_agents

        # creating the sublists
        sublists = []
        start = 0
        for i in range(self.nb_agents):
            #deciding if the sublist needs an extra element added to it or not
            if i < extra:
                end = start + base_size + 1
            else:
                end = start + base_size
            
            #adding the new sublist to the list of sublists
            sublists.append(self.nodes_idx_list[start:end])
            start = end

        # the first sublist is always the biggest, 
        # we take it as a the reference size
        target_size = len(sublists[0])

        # for all the other sublists (except the 1st one)
        for idx,sub_list in enumerate(sublists[1:]):
            
            # while it hasn't reached the desired length
            while len(sub_list) < target_size:

                # we choose a random node to add 
                random_node = rd.choice(list(self.nodes_idx_list)) #NOSONAR
                sub_list = np.append(sub_list,random_node)
            
            #updating the sublist with the corrected one
            sublists[idx+1] = sub_list

        return sublists

    def are_all_nodes_visited(self, individual: np.ndarray) -> bool:
        """
        Checks if an individual covers all the nodes of the Graph at least once

        Args:
            individual: The individual which has to be checked.

        Returns:
            bool: True -> all the nodes of the Graph are, at least once, visited.
            bool: False -> one or more nodes are not being visited by the individual.
        """

        # creating an empty set to store the visited nodes
        visited_nodes = set()

        for gene in individual:
            for node in gene:
                # we add the visited nodes to the corresponding set
                visited_nodes.add(node)

        # creating a set of the nodes the individuals have to cover
        nodes_to_cover = set(self.nodes_idx_list)

        # if the sets are equal, the individual covered all the nodes
        # thus the individual is valid
        if nodes_to_cover <= visited_nodes:
            return True
        else:
            return False

    def get_real_population_from_indicative_population(self) -> np.ndarray:
        """
         Gives the "real" paths using the "indicative" ones for the whole population.

        Returns:
            ndarray: Indicative_paths_populations-like matrix
                    containing the real paths for each indicative path.
        """

        # Create matrix of same shape
        shape_of_indicative_pop = self.indicative_paths_population.shape
        real_paths_population = np.empty((shape_of_indicative_pop[0], shape_of_indicative_pop[1]), dtype=object)

        # For each individual
        for idx_individual, individual in enumerate(self.indicative_paths_population):
            # For each path
            for idx_path, path in enumerate(individual):
                new_real_path = []

                # For each node in the path
                for i in range(len(path)):
                    # Retrieve the current node and the next node (wrap around with %)
                    origin, destination = path[i], path[(i + 1) % len(path)]

                    # Skip if origin and destination are the same
                    if origin == destination:
                        continue

                    # Retrieve the shortest path between origin and destination
                    shortest_path = list(self.shortest_way_dict[(origin, destination)])

                    # Append the nodes from the shortest path to the real path
                    # skipping the first if already added
                    if new_real_path and new_real_path[-1] == shortest_path[0]:
                        new_real_path.extend(shortest_path[1:])
                    else:
                        new_real_path.extend(shortest_path)

                # Remove the last node to avoid duplicating
                # the initial node at the end of the cycle
                if new_real_path and new_real_path[-1] == new_real_path[0]:
                    new_real_path.pop()

                # Store the real path
                real_paths_population[idx_individual][idx_path] = new_real_path

        return real_paths_population

    def path_lengths_computing(self, path: np.ndarray) -> float:
        """
        Computes the total length of a path.

        Args:
            path: The path for which the total length has to be computed.

        Returns:
            float: The total length of a path.
        """

        # contains the final value of the path
        eval_distance = 0
        for i in range(len(path) - 1):
            # we retrieve the actual node and the following one
            origin, destination = path[i], path[i + 1]
            # we add the intermediate distance to the final distance of the path
            eval_distance += self.distance_matrix[origin][destination]

        return eval_distance

    def mean_node_occurrence_computing(self, individual: np.ndarray) -> np.ndarray:
        """
        Computes the mean occurrence of each node in the individual.

        Args:
            individual: The individual for which the mean node occurrence has to be computed.

        Returns:
            float: The mean node occurrence for the individual.
        """

        list_of_occurrences = []
        flattened_individual = []

        for path in individual:
            for node in path:
                # if the current node is the list of the intermediate paths from node A to B
                if isinstance(node, list):
                    flattened_individual.extend(node)
                else:  # if not, we append it
                    flattened_individual.append(node)

        # for each node of the graph, we compute the occurrence
        for node in self.nodes_idx_list:
            # we count its occurrence in the individual
            occurrences = np.count_nonzero(flattened_individual == node)
            list_of_occurrences.append(occurrences)

        # then we compute the mean occurrence of the nodes in the individual
        mean_node_occurrence = np.mean(list_of_occurrences)

        return mean_node_occurrence

    def mean_path_lengths_computing(self, individual: np.ndarray) -> np.ndarray:
        """
        Computes the mean length of each path in the individual.

        Args:
            individual: The individual for which the mean path length has to be computed.

        Returns:
            float: the mean path length of the individual.
        """

        path_lengths = []
        # for each path of the individual
        for path in individual:
            # we append the length of the whole path
            path_lengths.append(self.path_lengths_computing(path))

        # then we compute the mean length of the paths
        path_length_mean = np.mean(path_lengths)
        return path_length_mean

    def fitness(self) -> list[tuple[float, float]]:
        """
        Awards a fitness to each individual
        using the mean occurrence and mean path length.

        Returns:
            A list of tuples (mean_node_occurrence, mean_distance).
        """
        fitness_lst = []

        for indicative_individual, real_individual in zip(self.indicative_paths_population, self.real_paths_population):

            # if the individual is valid
            if self.are_all_nodes_visited(indicative_individual):

                # we compute it's mean node recurrence using the real paths
                mean_node_occurrence = self.mean_node_occurrence_computing(real_individual)
                # and the mean path length using the indicative population
                # ( would've given the same value if we used the real paths instead)
                mean_path_length = self.mean_path_lengths_computing(indicative_individual)

                # computing the fitness itself
                fitness_value = (mean_node_occurrence, mean_path_length)

            # if he's not, we apply the worst possible fitness to him
            else:
                # in our case, we give it infinite
                fitness_value = (-float('inf'), float('inf'))

            # we append the fitness to a list of all the fitness's of the population
            fitness_lst.append(fitness_value)

        return fitness_lst

    def dominates(
            self, 
            individual_1: tuple[float, float], 
            individual_2: tuple[float, float]
        ) -> bool:
        """
        Checks if an individual dominates another individual

        Args:
            individual_1 : (mean_node_occurrence, mean_distance) of individual 1.
            individual_2 : (mean_node_occurrence, mean_distance) of individual 2.

        Returns:
            bool: True if individual_1 dominates individual_2.
            bool: False if there is no domination.
        """
        # verifying if the 2nd individual is dominating the 1st
        if individual_1[0] <= individual_2[0] and individual_1[1] <= individual_2[1]:

            # verifying that the 2 individuals aren't equal (would mean they're equivalent)
            if individual_1 != individual_2:
                # they are not equal, so there is a domination
                return True
            else:
                # they are equal, so NO domination
                return False
        else:
            # not respecting the domination condition, so no domination
            return False

    def pareto_fronts(self, fitness_list: list[tuple[float, float]]) -> list:
        """
        Classifies all the individuals of the population
        into categories from the best to the worst.

        It is using the Pareto Efficiency concept to achieve this.
        https://en.wikipedia.org/wiki/Pareto_front

        Args:
            fitness_list : The list containing th fitness of the population.

        Returns:
            A list of fronts where the first front contains the most balanced individuals
            1st front : the best individuals.
            last front: the worst individuals.
        """

        # output
        fronts = []

        # index list of all remaining individuals to "categorize"
        remaining_individual_indices = list(range(len(self.indicative_paths_population)))

        while remaining_individual_indices:

            # storing the current front
            current_front = []

            # for each remaining individual
            for index_1 in remaining_individual_indices:
                is_dominated = False

                # verifying if he's dominated by another individual
                for index_2 in remaining_individual_indices:

                    # if he is dominated, we break out of this loop
                    if self.dominates(fitness_list[index_2], fitness_list[index_1]):
                        is_dominated = True
                        break

                        # if he is not dominated, he will be part of the actual front
                if not is_dominated:
                    current_front.append(index_1)

            # adding the corresponding matrices for the current front
            current_front_matrices = []
            for i in current_front:
                current_front_matrices.append(self.indicative_paths_population[i])

            # adding the finished front to the fronts list
            fronts.append(current_front_matrices)

            # removing the indices of the actual front in the "remaining indices" list
            remaining_indices_new = []
            for i in remaining_individual_indices:
                if i not in current_front:
                    remaining_indices_new.append(i)

            # updating the list
            remaining_individual_indices = remaining_indices_new

        return fronts

    def selection_with_pareto(
                        self, 
                        fitness: list[tuple[float, float]], 
                        nb_parent: int
                    ) -> np.ndarray:
        """
        Selects the best individuals until reaching the desired number of parents.

        Args:
            fitness : The list containing th fitness of the population.
            nb_parent: The number of desired parents.

        Returns:
            np.ndarray: an array containing the best individuals
                        to be used for crossing and mutating.
        """

        selected_individuals = []

        # getting the pareto fronts
        fronts = self.pareto_fronts(fitness)

        for front in fronts:
            # checking if we can add the whole front
            if len(selected_individuals) + len(front) <= nb_parent:
                # adding it
                selected_individuals.extend(front)
            else:
                # if not, we only add what we need, then we get out of the loop
                remaining_slots = nb_parent - len(selected_individuals)
                selected_individuals.extend(front[:remaining_slots])
                break

        # casting it to a ndarray for later
        selected_individuals = np.array(selected_individuals)

        return selected_individuals

    def vertical_crossing_process(
                            self, 
                            parent_1: np.ndarray, 
                            parent_2: np.ndarray, 
                            nb_crossings: int
                        ) -> tuple[np.ndarray, np.ndarray]:
        """
        Crosses two individuals on a vertical axis.

        Args:
            parent_1 : The first parent to cross.
            parent_2 : The second parent to cross.
            nb_crossings: The number of crossings to apply on each parent.

        Returns:
            A tuple containing both created children.
        """
        # cutting the first individual vertically
        # according to the number of crossing we have to get
        sub_matrices_first_individual = np.array_split(parent_1, nb_crossings, axis=1)

        # cutting the second individual vertically
        # according to the number of crossing we have to get
        sub_matrices_second_individual = np.array_split(parent_2, nb_crossings, axis=1)

        # before applying the crossing method,
        # we shuffle the sub_matrices of the 2nd parent
        shuffled_sub_matrices = []
        for sub_matrix in sub_matrices_second_individual:
            #shuffling the lines of the matrices 
            shuffled_matrix = sub_matrix[np.random.permutation(sub_matrix.shape[0]), :] 
            shuffled_sub_matrices.append(shuffled_matrix)

        sub_matrices_second_individual = shuffled_sub_matrices

        temp_child_1 = []
        temp_child_2 = []

        # reassembling the children using an alternating pattern
        for i in range(nb_crossings):
            if i % 2 == 0:  # even index
                temp_child_1.append(sub_matrices_first_individual[i])
                temp_child_2.append(sub_matrices_second_individual[i])
            else:  # odd index
                temp_child_1.append(sub_matrices_second_individual[i])
                temp_child_2.append(sub_matrices_first_individual[i])

        # merging to get the children
        first_children = np.hstack(temp_child_1)
        second_children = np.hstack(temp_child_2)

        return first_children, second_children

    def optimize_child(self, child: np.ndarray) -> np.ndarray:

        """
        Optimizes a child by rearranging each path's nodes
        to get the shortest possible paths.

        Args:
           child : The child that has to be optimized.
           
        Returns:
            the optimized child.
        """
         
        optimized_child = []
        
        for path in child:
            # initializing hte optimal path with the first node of the path
            optimized_path = [path[0]]
            #keeping all the nodes expect the 1st one
            remaining_nodes = path[1:].tolist() 
            
            # Initialiser la distance minimale à l'infini
            while remaining_nodes:
                #getting the last node that has been added to the optimal path
                last_node = optimized_path[-1]
                
                #the current best node 
                optimal_node = None
                optimal_distance = float('inf')  
                
                # finding the nearest node
                for node in remaining_nodes:
                    distance_to_next_node = self.distance_matrix[last_node][node]
                    #if the distance is lower, we update the best node
                    if distance_to_next_node < optimal_distance:
                        optimal_node = node
                        optimal_distance = distance_to_next_node
                
                # then, we add the optimal node to the path
                optimized_path.append(optimal_node)
                # we remove it from the remaining choices
                remaining_nodes.remove(optimal_node) 

            # we add the optimal path
            optimized_child.append(optimized_path)
        
        return np.array(optimized_child)

    def child_validation_process(self, child: np.ndarray) -> np.ndarray:

        """
        Verifies if the generated child is valid, corrects him if necessary.

        Args:
            child : the child that has to be validated.

        Returns:
            The valid children.
        """

        # if the child is valid, we simply return him
        if self.are_all_nodes_visited(child):
            return child
        else:

            visited_nodes = []  # list containing the visited nodes in the child
            duplicates = []  # list of (i,j) coordinates of all the duplicate nodes contained in the child

            # as he's not valid,
            # we set up a list containing all the duplicate nodes contained n the child
            for idx_gene, gene in enumerate(child):
                for idx_node, node in enumerate(gene):
                    if node not in visited_nodes:
                        visited_nodes.append(node)
                    else:
                        duplicates.append((idx_gene, idx_node))

            # getting all the missing (= non-visited) nodes in the child
            visited_nodes = np.array(visited_nodes)
            missing_nodes = np.setdiff1d(self.nodes_idx_list, visited_nodes)

            # for every missing node, we add it at the coordinates of a duplicat node.
            for node in missing_nodes:
                # deleting the first element as he'll be replaced with a new value
                node_to_replace = duplicates.pop(0)

                # replacing the duplicate node by one of the missing nodes
                child[node_to_replace[0]][node_to_replace[1]] = node

            return child

    def crossing(self, parents: np.ndarray, nb_children: int) -> np.ndarray:
        """
        The whole crossing process..

        Args:
            parents : The list containing the parents.
            nb_children: The desired number of children.

        Returns:
            ndarray: A list containing all the children.
        """

        # matrix of same shape
        children = np.empty((nb_children, parents.shape[1], parents.shape[2]))

        i = 0

        while (i < nb_children):

            # probability of sterile parent
            x = rd.random()  # NOSONAR
            if x > self.crossing_rate:
                continue

            # randomly choosing the 2 individuals to cross together
            first_individual_to_cross = rd.randint(0, len(parents) - 1)  # NOSONAR
            second_individual_to_cross = rd.randint(0, len(parents) - 1)  # NOSONAR

            # assuring we don't choose the same individual twice
            # (no point doing that when crossing)
            while first_individual_to_cross == second_individual_to_cross:
                second_individual_to_cross = rd.randint(0, len(parents) - 1)  # NOSONAR

            # getting the parents
            parent1 = parents[first_individual_to_cross]
            parent2 = parents[second_individual_to_cross]

            # get the 2 created children
            created_children = list(self.vertical_crossing_process(parent1, parent2, self.number_of_crossing_points))

            # for each generated children
            # he passes through the validation process
            for new_child in created_children:
                #if the number of children is hit, we break
                if i == nb_children:
                    break
                else:
                    #we verify the child's validity
                    valid_child = self.child_validation_process(new_child) 
                    #then we optimize him   
                    children[i] = self.optimize_child(valid_child)            
                i += 1

        return children.astype(int)

    def mutating(self, children: np.ndarray) -> np.ndarray:
        """
        Mutates individuals if needed.

        Args:
            children: the list containing the children.
        Returns:
            ndarray: A list containing every child (mutated or not)
        """
        # matrix of same shape
        mutants = np.zeros(children.shape)

        # for each child
        for i in range(mutants.shape[0]):

            # probability of mutating
            random_value = rd.random()  # NOSONAR
            if random_value > self.mutation_rate:
                # continue
                pass

            # generate a random value associated for deciding which path will be mutated
            idx_col_to_shuffle = rd.randint(0, mutants.shape[1] - 1)  # NOSONAR

            # we reverse the right path of the child
            children[i][idx_col_to_shuffle] = np.flip(children[i][idx_col_to_shuffle])
            # we add the child to the mutants output
            mutants[i] = children[i]

        return mutants.astype(int)

    def find_best_individual(self, tuples_list: list[tuple[float, float]]) -> int:
        """
        find the best individual (the highest occurrence, lowest length).

        Args:
            tuples_list : the list containing the tuples
                          (in our case it's the list of the fitness's)

        Returns:
            tuple: the tuple having the highest mean occurrence and lowest mean length
                   or None if the list of tuples is empty
        """
        # if the list is empty
        if not tuples_list:
            return 0
        
        # getting the best individual by checking
        # the max mean occurrence and min mean length
        best_solution = (-999999,9999999)

        for tuple in tuples_list:
            
            #checking if actual individual is better than the actual best 
           if (tuple[0] > best_solution[0]) and (tuple[1] < best_solution[1] ):
                best_solution = tuple

        # looping over the elements of the list until we find the "best individual"
        for list_idx, list_tuple in enumerate(tuples_list):
            if list_tuple == best_solution:
                return list_idx

    def clean_output_individual(self, individual: np.ndarray) -> np.ndarray:
        """
        Cleans the individual which will be returned by the algorithm.
        Sometimes the optimal individual contains a repeated node in the middle.
        Sometimes he can also contain the same node as the first one at the end.
        EG:
            input: [37, 1, 3, 9, 6, 49, 49, 6, 9, 3, 1, 37]
            will become: [37, 1, 3, 9, 6, 49, 6, 9, 3, 1]

        Args:
            individual: The individual which has to be cleaned.

        Returns:
            ndarray: the cleaned individual
        """

        # New array for storing the cleaned output
        cleaned_individual = []

        for path in individual:
            # Check if the first and last nodes are the same
            # If yes, remove the last node to ensure the path is valid
            if path[0] == path[-1]:
                path = np.delete(path, -1)

            # Create a new path without consecutive duplicates
            cleaned_path = []
            for node in path:
                # Verify if a node is repeating itself right after the first occurrence
                # Example:
                #   -> 1, 2, 3 is OK
                #   -> 1, 2, 2, 3 is NOT OK
                # If the current node is not equal to the last added node, add it
                if not cleaned_path or cleaned_path[-1] != node:
                    cleaned_path.append(node)

            # Store the "cleaned" path
            cleaned_individual.append(cleaned_path)

        # Cast the result to an ndarray
        cleaned_individual = np.array(cleaned_individual, dtype=object)

        return cleaned_individual

    def launch(self) -> list:
        """
        Launches the whole Algorithm.

        Returns:
            the optimal individual which should
            in theory guarantee a minimal idleness during the simulation.
        """

        # generating the initial population
        self.indicative_paths_population = self.initial_population_generation()
        self.real_paths_population = self.get_real_population_from_indicative_population()

        # declaring the number of parents and thus, the number of children
        nbr_parents = self.nb_individuals_in_pop // 2
        nbr_enfants = self.nb_individuals_in_pop - nbr_parents

        for _ in range(self.nb_generations):

            # evaluating the fitness of the current population
            fitness = self.fitness()

            # selecting the best individuals to use them as parents
            parents = self.selection_with_pareto(fitness, nbr_parents)

            # crossing the parents to get children
            children = self.crossing(parents, nbr_enfants)

            # mutating the children to get mutants
            mutants = self.mutating(children)

            # updating the "indicative" population
            self.indicative_paths_population[0:parents.shape[0], :] = parents
            self.indicative_paths_population[parents.shape[0]:, :] = mutants

            # updating te "real paths" population
            self.real_paths_population = self.get_real_population_from_indicative_population()

        # evaluating the fitness of the final population
        fitness_finale = self.fitness()

        # index of the best individual of the final population
        best_individual_idx = self.find_best_individual(fitness_finale)

        # retrieving the best individual
        res_of_algo = self.indicative_paths_population[best_individual_idx]

        # cleaning the individual before returning him
        # also casting the ndarray to a list
        algorithm_output = list(self.clean_output_individual(res_of_algo))

        return algorithm_output