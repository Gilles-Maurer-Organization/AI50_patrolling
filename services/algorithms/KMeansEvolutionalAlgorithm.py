
import random as rd
import numpy as np

class KMeansEvolutionalAlgorithm: 

    def __init__(
        self, 
        nb_nodes : int, 
        distances : np.ndarray[np.ndarray[float]],
    ) -> None:

        self._nb_nodes = nb_nodes
        self._distances = distances

        self._nb_generations = 600
        self._pop_size = 40
        self._crossover_rate = 0.8
        self._mutation_rate = 0.2
        self._population = np.empty((self._pop_size, self._nb_nodes))

        
    def run(self) -> tuple[np.ndarray[int], float]:
        """
        Run the genetic algorithm to solve a TSP problem.
        """
        self._init_ag()
        return self._optimize()


    def _init_ag(self) -> None: 
        """
        Initialize the population of the genetic algorithm.
        Create first individual by using the nearest neighbour heuristic.
        Generate the rest of the population by mutation of the first individual.
        """
        first_individual = np.empty(self._nb_nodes)
        
        already_visited = set()
        not_visited = [i for i in range(self._nb_nodes)] 
        not_visited = set(not_visited)

        current_node = not_visited.pop()
        already_visited.add(current_node)
        first_individual[0] = current_node

        k = 1

        while len(not_visited) > 0:

            next_node = self._closest_neighbour(current_node, not_visited)
            not_visited.remove(next_node)
            already_visited.add(next_node)
            current_node = next_node
            first_individual[k] = current_node
            k += 1


        self._population[0] = first_individual

        for i in range(1, self._pop_size):
            individual = self._individual_mutation(first_individual)
            self._population[i] = individual
        
        self._population = self._population.astype(int)


    def _closest_neighbour(
        self, 
        current_node : int, 
        not_visited : set[int]
    ) -> int:
        """
        Find the closest neighbour of a node.

        Args:
            current_node : int : the current node
            not_visited : set[int] : the set of not visited nodes

        Returns:
            int : the closest neighbour of the current node
        """
        min_distance = 999999
        closest_node = -1

        for node in not_visited:
            distance = self._distances[current_node][node]
            if distance < min_distance:
                min_distance = distance
                closest_node = node

        return closest_node


    def _optimize(self) -> tuple[np.ndarray[int], float]:
        """
        Run the genetic algorithm to solve the TSP problem.

        Returns:
            sol_opt : np.ndarray[int] : the optimal solution
            min_fitness : float : the minimum distance
        """
        nbr_parents = self._pop_size // 2
        nbr_children = self._pop_size - nbr_parents 
       
        for _ in range(self._nb_generations):
            
            fitness = self._compute_fitness()

            parents = self._selection(fitness, nbr_parents)
            children = self._crossover(parents, nbr_children)
            mutants = self._mutation_rsm(children)

            
            self._population[0:parents.shape[0]] = parents
            self._population[parents.shape[0]:, :] = mutants

            
        fitness_derniere_generation = self._compute_fitness()   
        
        min_fitness = np.min(fitness_derniere_generation)
        index_min_fitness = np.nonzero(fitness_derniere_generation == min_fitness)
        sol_opt = self._population[index_min_fitness[0][0],:]
        
        return sol_opt, min_fitness


    def _compute_fitness(self) -> np.ndarray[float]:
        """
        Compute the fitness of each individual in the population.

        Returns:
            np.ndarray[float] : the fitness of each individual
        """
        fitness = np.empty(self._population.shape[0])

        for i in range(self._population.shape[0]):
            eval_distance=0
            solution = self._population[i]
            for j in range (len(solution)):
                origine, destination = solution[j], solution[(j+1)%self._nb_nodes]
                eval_distance += self._distances[origine][destination]
            fitness[i] = eval_distance
        
        return fitness.astype(float)


    def _selection(
        self, 
        fitness : np.ndarray[float], 
        nbr_parents : int
    ) -> np.ndarray[np.ndarray[int]]:
        """
        Select the parents of the next generation by using the roulette wheel selection.

        Args:
            fitness : np.ndarray[float] : the fitness of each individual
            nbr_parents : int : the number of parents to select

        Returns:
            np.ndarray[np.ndarray[int]] : the selected parents
        """
        min_fitness = np.min(fitness)
        fitness = fitness - min_fitness + 1

        total_fitness = np.sum(1 / fitness)
        probabilities = (1 / fitness) / total_fitness
        indices = np.random.choice(range(len(self._population)), size=nbr_parents, p=probabilities, replace=False)
        parents = self._population[indices]

        return parents


    def _mutation_rsm(
        self, 
        children : np.ndarray[np.ndarray[int]]
    ) -> np.ndarray[np.ndarray[int]]:
        """
        Apply the mutation to the children by using the RSM mutation.

        Args:
            children : np.ndarray[np.ndarray[int]] : the children

        Returns:
            np.ndarray[np.ndarray[int]] : the mutated children
        """
        
        mutants = np.empty((children.shape))
        
        for i in range(mutants.shape[0]):

            if rd.random() > self._mutation_rate:
                mutants[i] = children[i].copy()
            
            else: 
                mutants[i] = self._individual_mutation(children[i])

        return mutants 


    def _individual_mutation(
        self, 
        child : np.ndarray[np.ndarray[int]]
    ) -> np.ndarray[np.ndarray[int]]: 
        """
        Apply the RSM mutation to an individual.

        Args:
            child : np.ndarray[int] : the individual

        Returns:
            np.ndarray[int] : the mutated individual
        """

        if (child.shape[0] < 3):
            return child.copy()
        
        point_a = rd.randint(0, child.shape[0] - 3)
        point_b = rd.randint(point_a + 1, child.shape[0] - 1)

        inverted_segment = child[point_a:point_b].copy()               
        inverted_segment = np.flip(inverted_segment)

        mutant = child.copy()

        for i in range(point_a, point_b):
            mutant[i] = inverted_segment[i - point_a]

        return mutant


    def _crossover(
        self, 
        parents : np.ndarray[np.ndarray[int]],
        nbr_children : int
    ) -> np.ndarray[np.ndarray[int]]:
        """
        Apply the crossover to the parents by using the PMX crossover.

        Args:
            parents : np.ndarray[np.ndarray[int]] : the parents
            nbr_children : int : the number of children to create

        Returns:
            np.ndarray[np.ndarray[int]] : the children
        """ 
        children = np.empty((nbr_children, parents.shape[1]))
        nb_children_create = 0

        for nb_children_create in range(nbr_children):

            rd_parent1 = parents[rd.randint(0, parents.shape[0] - 1)].copy()
            rd_parent2 = parents[rd.randint(0, parents.shape[0] - 1)].copy()

            if rd.random() > self._crossover_rate or parents.shape[1] < 3: 
                children[nb_children_create] = rd_parent1

            else:

                point_a = rd.randint(0, parents.shape[1] - 3)
                point_b = rd.randint(point_a + 1, parents.shape[1] - 1)

                child = np.full(rd_parent1.shape, -1)

                heritage_parent1 = rd_parent1[point_a:point_b].copy()
                not_in_h1 = []

                for i in range(child.shape[0]):
                    if rd_parent2[i] not in heritage_parent1:
                        not_in_h1.append(rd_parent2[i])

                child[point_a:point_b] = heritage_parent1

                child = self._complete_child(child, not_in_h1)
                
                children[nb_children_create] = child

        return children
    

    def _complete_child(
        self, 
        child : np.ndarray[int], 
        not_in_h1 : list[int]
    ) -> np.ndarray[int]: 
        """
        Complete the child by adding the missing nodes (part of the crossover).

        Args:
            child : np.ndarray[int] : the child
            not_in_h1 : list[int] : the missing nodes

        Returns:
            np.ndarray[int] : the child with the missing nodes
        """

        index = 0

        for i in range(child.shape[0]):
            if  child[i] == -1:
                child[i] = not_in_h1[index]
                index += 1

        return child

