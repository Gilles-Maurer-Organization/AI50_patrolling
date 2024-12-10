import numpy as np 
import random as rd
import time
from services.algorithms.IAlgorithm import IAlgorithm
from models.Graph import Graph

class  EvolutionalAlgorithm(IAlgorithm):
    """
    This class implements a regular Genetics Algorithm.
    
    Attributes:
        -> nb_generations : The number of generation the Algorithm has to perform.
        -> nb_agents : The number of agents (defines the size of an individual).
        -> nb_individuals_in_pop : The number of individuals in the population.
        -> indicative_paths_population : Contains the "short" version of the path, thus ignoring the case when 2 following nodes in the path don't have a direct link. 
        -> real_paths_population : Contains the "real" path by adding the additional nodes between 2 nodes which don't have a direct link
        -> shortest_way_dict : the "shortest_paths" attribute from the Graph Class.
        -> distance_matrix  : the "complete_adjacency_matrix" attribute from the Graph Class.
        -> nodes_idx_list : Stores a sorted list of all the nodes contained the Graph.

    Methods:

        ---population---

            initial_population_generation :
                Generates a random initial population for the Algorithm.

            are_all_nodes_visited :
                Checks if an individual covers all the nodes of the Graph at least once.

            get_real_population_from_indicative_population :
                Gives the "real" paths using the "indicative" ones for the whole population.

        ---fitness---

            path_lengths_computing :
                Computes the total length of a path.

            mean_node_occurrence_computing :
                Computes the mean occurrence of each node in the individual.

            mean_path_lengths_computing :
                Computes the mean length of each path in the individual.

            fitness :
                Awards a fitness to each individual (using the mean occurrence and mean path length).

        ---selection---

            dominates :
                Checks if an individual dominates another individual.

            pareto_fronts :
                Classifies all the individuals of the population into categories from the best to the worst.

            selection_with_pareto :
                Selects the best individuals until reaching the desired number of parents.

        ---crossing---

            vertical_crossing_process :
                Crosses two individuals on a vertical axis.

            child_validation_process:
                Verifies if the generated child is valid, corrects him if necessary.

            crossing :
                The whole crossing process.

        ---mutation---

            mutating :
                Mutates individuals if needed.

        ---final output---

            find_best_individual :
                Find the best individual (highest occurrence, lowest length).

            clean_output_individual :
                Cleans the individual which will be returned by the algorithm.

        ---launch of the Algorithm---

            launch :
                Launches the whole Algorithm.

    """

    # The "# NOSONAR" comments you'll see next to the random number generators are used to tell SonarCloud to skip the associated warnings 
    # as the random generators are used on purpose.

    def __init__(self, nb_of_generations, nb_agent, individuals_number_per_population, graph_object):
        self.nb_generations = nb_of_generations
        self.nb_agents = nb_agent
        self.nb_individuals_in_pop = individuals_number_per_population
        self.indicative_paths_population = []  
        self.real_paths_population = [] 
        self.shortest_way_dict = graph_object.get_shortest_paths()
        self.distance_matrix = graph_object.get_complete_adjacency_matrix()
        self.nodes_idx_list = np.arange(0, len(graph_object.get_complete_adjacency_matrix()))

    #à revoir en vrai 
    def initial_population_generation(self): 
        """
        Generates a random initial population for the Algorithm.
        Also verifies that the generated individual is indeed valid, thus helps the algorithm for converging faster 

        Returns:
            ndarray: the generated indicative population.
        """

        #the length of 1 gene of the individual
        #TODO: ajuster le param gene_length
        gene_length = max(1, int( 0.75 * len(self.nodes_idx_list)))  #ajuster le 0.25 dynamiquement ici (jsp comment ) ...
        #gene_length = max(1, int(len(self.nodes_idx_list)/self.nb_agents))
        print(gene_length)
        indicative_population = []

        # For each individual
        for _ in range(self.nb_individuals_in_pop):

            #while the individual is not covering all nodes, we generate him
            while True:

                individual = []
                # For each gene of the individual (a gene is a path of an agent)
                for _ in range(self.nb_agents):

                    #while the generated gene already exists, we generate another one (max 10 tries)
                    nb_tries_agent = 0
                    while (nb_tries_agent < 10):
                        # Generate a random individual of the desired length
                        random_individual = rd.sample(self.nodes_idx_list.tolist(), gene_length) #NOSONAR
                        # Ensure the generated path does not already exist in the individual's genes
                        if random_individual not in individual:
                            individual.append(random_individual)
                            break
                        else:
                            nb_tries_agent+=1

                #verifying of the indiviual covers all nodes at least once
                if self.are_all_nodes_visited(individual):
                    # Appending the individual to the population if he's OK 
                    indicative_population.append(individual)
                    break

        # Transforming into np.array for later use
        indicative_population = np.array(indicative_population)    
        return indicative_population
 
    def are_all_nodes_visited(self, individual):
        """
        Checks if an individual covers all the nodes of the Graph at least once.

        Args:
            individual: The individual which has to be checked.

        Returns:
            bool: True if all the nodes of the Graph are, at least once, visited.
            bool: False if one or more nodes are not being visited by the individual.
        """

        #creating an empty set to store the visited nodes
        visited_nodes = set()

        for gene in individual:
            for node in gene:
                #we add the visited nodes to the corresponding set
                visited_nodes.add(node)

        #creating a set of the nodes the individuals have to cover
        nodes_to_cover = set(self.nodes_idx_list)

        #if the sets are equal, the individual covered all the nodes, thus the individual is valid
        if nodes_to_cover <= visited_nodes:
            return True
        else:
            return False

    def get_real_population_from_indicative_population(self):
        """
         Gives the "real" paths using the "indicative" ones for the whole population.

        Returns:
            ndarray: Indicative_paths_populations-like matrix containing the real paths for each indicative path.
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

                    # Retrieve the shortest path between origin and destination #TODO: passer le self.shortest_way_dict pour un dictionnaire
                    shortest_path = list(self.shortest_way_dict[(origin,destination)])

                    # Append the nodes from the shortest path to the real path, skipping the first if already added
                    if new_real_path and new_real_path[-1] == shortest_path[0]:
                        new_real_path.extend(shortest_path[1:])
                    else:
                        new_real_path.extend(shortest_path)

                # Remove the last node to avoid duplicating the initial node at the end of the cycle
                if new_real_path and new_real_path[-1] == new_real_path[0]:
                    new_real_path.pop()

                # Store the real path
                real_paths_population[idx_individual][idx_path] = new_real_path

        return real_paths_population

    def path_lengths_computing(self, path):
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

    def mean_node_occurrence_computing(self,individual):
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
                if isinstance(node, list):  #if the current node is the list of the intermediate paths from node a to b
                    flattened_individual.extend(node)
                else:  #if not, we append it 
                    flattened_individual.append(node)
                
        #for each node of the graph, we compute the occurrence
        for node in self.nodes_idx_list:
                    
            #we count it's occurrence in the individual
            occurrences = np.count_nonzero(flattened_individual == node)
            list_of_occurrences.append(occurrences)

        #then we compute the mean occurrence of the nodes in the individual
        mean_node_occurrence = np.mean(list_of_occurrences)
        
        return mean_node_occurrence

    def mean_path_lengths_computing(self,individual):
        """
        Computes the mean length of each path in the individual.

        Args:
            individual : The individual for which the mean path length has to be computed.

        Returns:
            float : the mean path length of the individual.
        """
         
        path_lengths = []
        #for each path of the individual
        for path in individual:
            #we append the length of the whole path
            path_lengths.append(self.path_lengths_computing(path))

        #then we coompute the mean length of the paths
        path_length_mean = np.mean(path_lengths)
        return path_length_mean 

    def fitness(self):
        """
        Awards a fitness to each individual using the mean occurrence and mean path length.

        Returns:
            A list of tuples (mean_node_occurrence, mean_distance). 
        """
        fitness_lst = []

        for indicative_individual, real_individual in zip(self.indicative_paths_population, self.real_paths_population):

            #if the individual is valid
            if self.are_all_nodes_visited(indicative_individual):
                
                #we compute it's mean node recurrence using the real paths
                mean_node_occurrence = self.mean_node_occurrence_computing(real_individual)
                #and the mean path length using the indicative population ( would've given the same value if we used the real paths instead)
                mean_path_length = self.mean_path_lengths_computing(indicative_individual)

                #computing the fitness itself
                fitness_value = (mean_node_occurrence, mean_path_length)
                
            #if he's not, we apply the worst possible fitness to him
            else:   
                #in our case, we give it infinite
                fitness_value = (-float('inf'),float('inf'))
            
            #we append the fitness to a list of all the fitnesses of the population 
            fitness_lst.append(fitness_value)
        
        return fitness_lst

    def dominates(self, individual_1, individual_2):
        """
        Checks if an individual dominates an other individual

        Args:
            individual_1 (tuple): (mean_node_occurrence, mean_distance) of individual 1.
            individual_2 (tuple): (mean_node_occurrence, mean_distance) of individual 2.

        Returns:
            bool: True if individual_1 dominates individual_2.
            bool: False if there is no domination.
        """
        #verifying if the 2nd individual is dominationg the 1st
        if individual_1[0] <= individual_2[0] and individual_1[1] <= individual_2[1]:

            # Vérifie que ind1 n'est pas exactement égal à ind2 (ce qui signifierait qu'ils sont équivalents)
            if individual_1 != individual_2:

                #they are not equal, so there is a domination
                return True  
            else:
                #they are equal, so NO domination
                return False  
        else:
            #not respecting the domination condition, so no domination
            return False  

    def pareto_fronts(self, fitness_list):
        """
        Classifies all the individuals of the population into categories from the best to the worst.
        It is using the Pareto Efficiency concept to achieve this. https://en.wikipedia.org/wiki/Pareto_efficiency

        Args:
            fitness_list : The list containing th fitness of the population.

        Returns:
            A list of fronts where the first front contains the most balanced individuals (= the best) and the last, the worst ones.
        """
         
        #output 
        fronts = [] 

        # index list of all remaining individuals to "categorize"
        remaining_individual_indices = list(range(len(self.indicative_paths_population)))  

        while remaining_individual_indices:

            #storing the current front
            current_front = [] 
            
            #for each remaining individual
            for index_1 in remaining_individual_indices:
                is_dominated = False  

                # verifying if he's dominated by an other individual
                for index_2 in remaining_individual_indices:
                    
                    #if he is dominated, we break out of this loop
                    if self.dominates(fitness_list[index_2], fitness_list[index_1]):
                        is_dominated = True  
                        break 

                # if he is not dominated, he will be part of the actual front
                if not is_dominated:
                    current_front.append(index_1)

            # adding the corresponding matrices fro the current front
            current_front_matrices = []
            for i in current_front:
                current_front_matrices.append(self.indicative_paths_population[i])
            
            #adding the finished front to the fronts list
            fronts.append(current_front_matrices)  

            #removing the indices of the actual front in the "remaining indices" list 
            remaining_indices_new = []
            for i in remaining_individual_indices:
                if i not in current_front:
                    remaining_indices_new.append(i)

            #updating the list
            remaining_individual_indices = remaining_indices_new  

        return fronts

    def selection_with_pareto(self, fitness, nb_parent):
        """
        Selects the best individuals until reaching the desired number of parents.

        Args:
            fitness : The list containing th fitness of the population.
            nb_parent: The number of desired parents.

        Returns:
            list: A list of fronts where the first front contains the most balanced individuals (= the best) and the last, the worst ones.
        """

        selected_individuals = []
    
        #getting the pareto fronts
        fronts = self.pareto_fronts(fitness)

        for front in fronts:
            #checking if we can add the whole front
            if len(selected_individuals) + len(front) <= nb_parent:
                #adding it
                selected_individuals.extend(front)
            else:
                #if not, we only add what we need, then we get out of the loop
                remaining_slots = nb_parent - len(selected_individuals)
                selected_individuals.extend(front[:remaining_slots])
                break

        #casting it to an ndarray for later 
        selected_individuals = np.array(selected_individuals)

        return selected_individuals

    def vertical_crossing_process(self, parent_1, parent_2, nb_crossings):
        """
        Crosses two individuals on a vertical axis.

        Args:
            parent_1 : The first parent to cross.
            parent_2 : The second parent to cross.
            nb_crossings: The number of crossings to apply on each parent.

        Returns:
            A tuple containing both created children.
        """
        #cutting the first individual vertically according to the number of crossing we have to get
        sub_matrices_first_individual = np.array_split(parent_1, nb_crossings, axis=1)  
            
        #cutting the second individual vertically according to the number of crossing we have to get
        sub_matrices_second_individual = np.array_split(parent_2, nb_crossings, axis = 1)  
            
        temp_child_1 = []  
        temp_child_2 = []  

        #reassembling the children using an alternating pattern 
        for i in range(nb_crossings):
            if i % 2 == 0:  # even index 
                temp_child_1.append(sub_matrices_first_individual[i])
                temp_child_2.append(sub_matrices_second_individual[i])
            else:  # odd index
                temp_child_1.append(sub_matrices_second_individual[i])
                temp_child_2.append(sub_matrices_first_individual[i])

        #merging to get the children
        first_children = np.hstack(temp_child_1)
        second_children = np.hstack(temp_child_2)

        return first_children, second_children

    def child_validation_process(self,child):

        """
        Verifies if the generated child is valid, corrects him if necessary.

        Args:
            child : the child that has to be validated.

        Returns:
            The valid children.
        """

        #if the child is valid, we simply return him
        if self.are_all_nodes_visited(child):
            return child
        else:

            visited_nodes = []  # list containing the visited nodes in the child
            duplicates = []  # contains a list of (i,j) coordinates of all the duplicate nodes contaned in the child

            # as he's not valid, we set up a list containing all the duplicate nodes contained n the child
            for idx_gene,gene in enumerate(child):
                for idx_node,node in enumerate(gene):
                    if node not in visited_nodes:
                        visited_nodes.append(node)
                    else:
                        duplicates.append((idx_gene,idx_node))

            # getting all the missing (= non-visited) nodes in the child
            visited_nodes = np.array(visited_nodes)
            missing_nodes = np.setdiff1d(self.nodes_idx_list,visited_nodes)

            #for every missing node, we add it at the coordinates of a duplicat node.
            for node in missing_nodes:
                # deleting the first element as he'll be replaced with a new value
                node_to_replace = duplicates.pop(0)

                #replacing the duplicate node by one of the missing nodes
                child[node_to_replace[0]][node_to_replace[1]] = node

            return child

    def crossing(self, parents, nb_children):
        """
        The whole crossing process..

        Args:
            parents : The list containing the parents.
            nb_children: The desired number of children.

        Returns:
            ndarray: A list containing all the children.
        """ 

        #matrix of same shape
        children = np.empty((nb_children,parents.shape[1],parents.shape[2])) 
        #TODO: determiner la meilleure valeur ici 
        number_of_crossing_points = 2 #we cut in 2 parts atm

        #probability of crossing the parents
        crossing_rate = 0.8
        i = 0
        nb_attempts = 0
        while (i < nb_children) :
            
            #probability of steril parent
            x = rd.random() # NOSONAR
            if x > crossing_rate:  
                continue

            #randomly choosing the 2 individuals to cross together
            first_individual_to_cross = rd.randint(0,len(parents)-1) # NOSONAR
            second_individual_to_cross = rd.randint(0,len(parents)-1) # NOSONAR

            #assuring we don't choose the same individual twice (no point doing that when crossing)
            while first_individual_to_cross == second_individual_to_cross:
                second_individual_to_cross = rd.randint(0,len(parents)-1) # NOSONAR

            #getting the parents
            parent1 = parents[first_individual_to_cross]
            parent2 = parents[second_individual_to_cross]

            #get the 2 created children
            created_children = list(self.vertical_crossing_process(parent1,parent2, number_of_crossing_points))

            #for each generated children, he passes through the validation process
            for new_child in created_children:
                children[i] = self.child_validation_process(new_child)
                i+=1


        return children.astype(int)
         
    def mutating(self, children):
        """
        Mutates individuals if needed.

        Args: 
            children: the list containing the children.
        Returns:
            ndarray: A list containing every children (mutated or not)
        """
        #matrix of same shape
        mutants = np.zeros((children.shape))

        #probability of mutating the child
        taux_mutation = 0.5

        #for each child
        for i in range(mutants.shape[0]):
            
            #probability of mutating
            random_value = rd.random() # NOSONAR
            if random_value > taux_mutation:
                #continue
                pass
                
            #generate a random value associated for deciding which path will be mutated
            idx_col_to_shuffle = rd.randint(0,mutants.shape[1]-1) # NOSONAR

            #we reverse the right path of the child
            children[i][idx_col_to_shuffle] = np.flip(children[i][idx_col_to_shuffle])
            #we add the child to the mutants output
            mutants[i] = children[i]

        return mutants.astype(int)
    
    def find_best_individual(self,tuples_list):
        """
        find the best individual (highest occurrence, lowest length).

        Args: 
            tuples_list : the list containing the tuples (in our case its the list of the fitnesses)
        Returns:
            tuple: the tuple having the highest mean occurrence and lowest mean length or None if the list of tuples is empty
        """
        #if the list is empty
        if not tuples_list:
            return None
        
        # getting the best individual by checking the max mean occurrence and min mean length
        best_individual =  max(tuples_list, key=lambda x: (x[0].max(), -x[1].min()))

        #looping over the elements of the list until we find the "best individual"
        for list_idx, list_tuple in enumerate(tuples_list):
            if list_tuple == best_individual:
                return list_idx

    def clean_output_individual(self, individual):
        """
        Cleans the individual which will be returned by the algorithm.
        Sometimes the optimal individual contains a repeated node in the middle.
        Sometimes he can also contain the same node as the first one at the end.
        EG: 
            input: [37, 1, 3, 9, 6, 49, 49, 6, 9, 3, 1, 37] 
            will become : [37, 1, 3, 9, 6, 49, 6, 9, 3, 1]

        Args:
            individual: The individual which has to be cleaned.

        Returns:
            ndarray: the cleaned individual
        """

        #new array for storing the cleaned output
        cleaned_individual =[]

        for path in individual:
            
            if path[0]==path[-1]:
                path = np.delete(path, -1)

            for i in range(len(path) - 1):
                #we verify if a node is repeating itself right after the first occurrence of the node
                #example: 
                #   ->  1,2,3 is OK 
                #   ->  1,2,2,3 is NOT OK 
                if path[i] == path[i + 1]:
                    #if it is indeed repeating, we delete the the second occurrence
                    path = np.delete(path, i + 1)
                    break  
                
            #storing the "cleaned" path
            cleaned_individual.append(list(path))

        #casting it to an ndarray
        cleaned_individual = np.array(cleaned_individual, dtype = object)

        return cleaned_individual

    def launch(self):
        """
        Launches the whole Algorithm.

        Returns:
            the optimal individual which should, in theory, guarantee a minimal idleness during the simulation.
        """

        #generating the initial population
        self.indicative_paths_population = self.initial_population_generation()
        self.real_paths_population = self.get_real_population_from_indicative_population()

        #declaring the number of parents and thus, the number of children
        nbr_parents = self.nb_individuals_in_pop // 2
        nbr_enfants = self.nb_individuals_in_pop - nbr_parents

        for _ in range(self.nb_generations):
            print("iter",_)
            #evaluating the fitness of the current population
            fitness = self.fitness()

            #---for testing
            if _ == 0:
                print("fitness initiale\n",fitness)
            #---

            #selecting the best individuals to use them as parents
            parents = self.selection_with_pareto(fitness,nbr_parents)

            #crossing the parents to get children
            children = self.crossing(parents, nbr_enfants)

            #mutating the children to get mutants
            mutants = self.mutating(children)

            # updating the "indicative" population
            self.indicative_paths_population[0:parents.shape[0], :] = parents  
            self.indicative_paths_population[parents.shape[0]:, :] = mutants

            #updating te "real paths" population
            self.real_paths_population = self.get_real_population_from_indicative_population()

        #evaluating the fitness of the final population
        fitness_finale = self.fitness()
        print("fitness finale\n",fitness_finale)
        #index of the best individual of the final population
        best_individual_idx = self.find_best_individual(fitness_finale)

        #retrieving the best individual
        res_of_algo = self.indicative_paths_population[best_individual_idx]

        #cleaning the individual before returning him
        algorithm_output = self.clean_output_individual(res_of_algo)

        return algorithm_output
        
       

if __name__ == "__main__":

    simple_graph = [
        [  0, 120, 190, 280,  95, 230, 290, 210, 270,  50],
       [120,   0,  70, 160, 160, 110, 170, 330, 150, 170],
       [190,  70,   0,  90, 230, 180, 100, 400, 230, 240],
       [280, 160,  90,   0,  75, 270, 190,  60, 320, 330],
       [ 95, 160, 230,  75,   0, 100, 330, 305, 310, 145],
       [230, 110,   0,  90, 100,   0,  90, 440, 260,  60],
       [290, 170, 100,   0, 330,  90,   0, 150, 330, 340],
       [210, 330, 400,  60, 305, 440, 150,   0,  70, 130],
       [270, 150, 230, 320, 310, 260, 330,  70,   0, 320],
       [ 50, 170, 240, 330, 145,  60, 340, 130, 320,   0]
    ]
    shortest_way_mat = [
        [[0],       [0, 1],    [0, 1, 2],    [0, 1, 2, 3], [0, 4],    [0, 1, 5],  [0, 1, 2, 6],  [0, 7],    [0, 1, 8],   [0, 9]],
        [[1, 0],     [1],      [1, 2],       [1, 2, 3],    [1, 4],    [1, 5],     [1, 2, 6],     [1, 0, 7], [1, 8],      [1, 0, 9]],
        [[2, 1, 0],  [2, 1],    [2],         [2, 3],       [2, 1, 4], [2, 1, 5],  [2, 6],        [2, 1, 0, 7], [2, 8],   [2, 1, 0, 9]],
        [[3, 2, 1, 0], [3, 2, 1], [3, 2],     [3],         [3, 2, 1, 4], [3, 2, 1, 5], [3, 2, 6], [3, 7], [3, 2, 8], [3, 2, 1, 0, 9]],
        [[4, 0],     [4, 1],    [4, 1, 2],    [4, 3],       [4],       [4, 5],     [4, 1, 2, 6], [4, 0, 7], [4, 1, 8], [4, 0, 9]],
        [[5, 1, 0],  [5, 1],    [5, 2],       [5, 2, 3],    [5, 4],     [5],       [5, 6],        [5, 1, 0, 7], [5, 1, 8], [5, 9]],
        [[6, 2, 1, 0], [6, 2, 1], [6, 2],     [6, 3],       [6, 2, 1, 4], [6, 5],  [6],          [6, 7],   [6, 2, 8], [6, 2, 1, 0, 9]],
        [[7, 0],     [7, 0, 1], [7, 0, 1, 2], [7, 3],       [7, 0, 4],   [7, 0, 5], [7, 6],        [7],     [7, 8],   [7, 0, 9]],
        [[8, 1, 0],  [8, 1],    [8, 2],       [8, 2, 3],    [8, 1, 4],  [8, 1, 5],  [8, 2, 6],    [8, 7],   [8],      [8, 1, 0, 9]],
        [[9, 0],     [9, 0, 1], [9, 0, 1, 2], [9, 0, 1, 2, 3], [9, 0, 4], [9, 5],  [9, 0, 1, 2, 6], [9, 0, 7], [9, 0, 1, 8], [9]]
    ]

    shortest_way_dict = {}
    for i in range(len(shortest_way_mat)):
        for j in range(len(shortest_way_mat)):
            shortest_way_dict[(i,j)] = shortest_way_mat[i][j]

    #for elem in shortest_way_dict:
        #print(elem, ": ",shortest_way_dict[elem] )


    #500, 5, 10, 10
    graph = Graph()
    graph.set_complete_adjacency_matrix(simple_graph)
    graph.set_shortest_paths(shortest_way_dict)
    
    AG =  EvolutionalAlgorithm(100, 10, 15, graph)

    for _ in range(10):
        print(_)
        start = time.time()
        res = AG.launch()
        end = time.time()-start

    print("REs algo G:")
    for elem in res:
        print(elem)
        print("---")

    print("temps :",end," secondes")
    