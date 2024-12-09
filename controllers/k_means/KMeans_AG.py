

import random as rd
import numpy as np
import matplotlib.pyplot as plt

class AlgorithmeGenetique: 

    def __init__(self, list_villes, distances):

        self.nb_villes = len(list_villes)
        self.list_villes = list_villes

        self.distances = distances

        self.nb_generations = 1000
        self.pop_size = 50

        self.population = np.empty((self.pop_size, self.nb_villes))

        
    def run(self):

        self.init_ag()
        return self.optimize()

    

    def init_ag(self): 

        first_individual = np.empty(self.nb_villes)
        
        already_visited = set()
        not_visited = [i for i in range(self.nb_villes)]
        not_visited = set(not_visited)

        current_city = not_visited.pop()
        already_visited.add(current_city)
        first_individual[0] = current_city

        k = 1

        while len(not_visited) > 0:

            next_city = self.closest_neighbour(current_city, not_visited)
            not_visited.remove(next_city)
            already_visited.add(next_city)
            current_city = next_city
            first_individual[k] = current_city
            k += 1


        self.population[0] = first_individual

        for i in range(1, self.pop_size):
            individual = self.individual_mutation(first_individual)
            self.population[i] = individual
        
        # print(f'Population initiale: \n{self.population}\n')

        self.population = self.population.astype(int)


    def closest_neighbour(self, current_city, not_visited):

        min_distance = 999999
        closest_city = -1

        for city in not_visited:
            distance = self.distances[current_city][city]
            if distance < min_distance:
                min_distance = distance
                closest_city = city

        return closest_city


    def optimize(self):
        nbr_parents = self.pop_size // 2
        nbr_enfants = self.pop_size - nbr_parents 

        x = [i for i in range(self.nb_generations)]
        y_min = np.zeros(self.nb_generations)
        y_avg = np.zeros(self.nb_generations)
        
        for gen in range(self.nb_generations):
            
            print(f"\rProgression : {(int)(gen * 100/self.nb_generations):.0f}%", end="")

            fitness = self.cal_fitness()

            y_min[gen] = np.min(fitness)
            y_avg[gen] = np.mean(fitness)

            # print(f'Voici la population: \n{self.population}\n')
            # print(f'Fitness de la population: \n{fitness}\n')

            parents = self.selection(fitness, nbr_parents)
            enfants = self.croisement(parents, nbr_enfants)
            mutants = self.mutation_rsm(enfants)

            
            self.population[0:parents.shape[0]] = parents
            self.population[parents.shape[0]:, :] = mutants

            
        fitness_derniere_generation = self.cal_fitness()   
        
        # print(f'Voici la dernière génération de la population: \n{self.population}\n') 
        # print(f'Fitness de la dernière génération: \n{fitness_derniere_generation}\n')

        # plt.plot(x, y_min, label='Minimum')
        # plt.plot(x, y_avg, label='Moyenne')
        # plt.xlabel('Générations')
        # plt.ylabel('Fitness')
        # plt.legend()
        # plt.show()

        min_fitness = np.min(fitness_derniere_generation)
        index_min_fitness = np.where(fitness_derniere_generation == min_fitness)
        sol_opt = self.population[index_min_fitness[0][0],:]
        
        print("\r", 20*" ")

        return sol_opt, min_fitness




    def cal_fitness(self):

        fitness = np.empty(self.population.shape[0])

        for i in range(self.population.shape[0]):
            eval_distance=0
            solution = self.population[i]
            for j in range (len(solution)):
                origine, destination = solution[j], solution[(j+1)%self.nb_villes]
                eval_distance += self.distances[origine][destination]
            fitness[i] = eval_distance
        
        return fitness.astype(float)


    def selection(self, fitness, nbr_parents):

        min_fitness = np.min(fitness)
        fitness = fitness - min_fitness + 1

        total_fitness = np.sum(1 / fitness)  # Priorité aux plus petites distances
        probabilities = (1 / fitness) / total_fitness
        indices = np.random.choice(range(len(self.population)), size=nbr_parents, p=probabilities, replace=False)
        parents = self.population[indices]
        return parents


    def mutation_rsm(self, enfants):
        
        mutants = np.empty((enfants.shape))
        taux_mutation = 0.2 # taux de mutation
        
        for i in range(mutants.shape[0]):

            if rd.random() > taux_mutation:
                mutants[i] = enfants[i].copy()
            
            else: 

                mutants[i] = self.individual_mutation(enfants[i])

        return mutants 


    def individual_mutation(self, enfant): 
        
        point_a = rd.randint(0, enfant.shape[0] - 3)
        point_b = rd.randint(point_a + 1, enfant.shape[0] - 1)

        inverted_segment = enfant[point_a:point_b].copy()               
        inverted_segment = np.flip(inverted_segment)

        mutant = enfant.copy()

        for i in range(point_a, point_b):
            mutant[i] = inverted_segment[i - point_a]

        return mutant



    def croisement(self, parents, nbr_enfants):

        enfants = np.empty((nbr_enfants, parents.shape[1]))
        taux_croisement = 0.7
        nb_enfants_create = 0

        for nb_enfants_create in range(nbr_enfants):

            rd_parent1 = parents[rd.randint(0, parents.shape[0] - 1)].copy()
            rd_parent2 = parents[rd.randint(0, parents.shape[0] - 1)].copy()

            if rd.random() > taux_croisement:
                enfants[nb_enfants_create] = rd_parent1

            else:

                point_a = rd.randint(0, parents.shape[1] - 3)
                point_b = rd.randint(point_a + 1, parents.shape[1] - 1)

                # remplir de -1
                enfant = np.full(rd_parent1.shape, -1)

                heritage_parent1 = rd_parent1[point_a:point_b].copy()
                not_in_h1 = []

                for i in range(enfant.shape[0]):
                    if rd_parent2[i] not in heritage_parent1:
                        not_in_h1.append(rd_parent2[i])

                enfant[point_a:point_b] = heritage_parent1
                index = 0

                for i in range(enfant.shape[0]):
                    if enfant[i] == -1:
                        enfant[i] = not_in_h1[index]
                        index += 1

                enfants[nb_enfants_create] = enfant



        return enfants

    




    #region ancien code

    
    # def croisement(self, parents, nbr_enfants):
    #     enfants = np.empty((nbr_enfants, parents.shape[1]))
    #     point_de_croisement = int(parents.shape[1]/2) #croisement au milieu
    #     taux_de_croisement = 0.8
    #     i = 0

    #     while (i < nbr_enfants): #parents.shape[0]
    #         indice_parent1 = i%parents.shape[0]
    #         indice_parent2 = (i+1)%parents.shape[0]
    #         x = rd.random()
    #         if x < taux_de_croisement: # probabilité de croisement

    #             indice_parent1 = i%parents.shape[0]
    #             indice_parent2 = (i+1)%parents.shape[0]
    #             enfants[i,0:point_de_croisement] = parents[indice_parent1,0:point_de_croisement]
    #             enfants[i,point_de_croisement:] = parents[indice_parent2,point_de_croisement:]
    #             i+=1

    #     return enfants



    # def selection(self, fitness, nbr_parents):
    #     fitness = list(fitness)
    #     parents = np.empty((nbr_parents, self.population.shape[1]))

    #     for i in range(nbr_parents):
    #         indice_min_fitness = np.where(fitness == np.min(fitness))
    #         parents[i,:] = self.population[indice_min_fitness[0][0], :]
    #         fitness[indice_min_fitness[0][0]] = 999999

    #     return parents



    
    # def mutation(self, enfants):
    #     mutants = np.empty((enfants.shape))
    #     taux_mutation = 0.3 # taux de mutation
        
    #     for i in range(mutants.shape[0]):
    #         random_valeur = rd.random()
    #         mutants[i,:] = enfants[i,:]
    #         if random_valeur < taux_mutation:

    #             random_index_1 = rd.randint(0, len(mutants[i]) - 2)
    #             random_index_2 = rd.randint(0, len(mutants[i]) - 2)

    #             val = mutants[i][random_index_1]
    #             mutants[i][random_index_1] = mutants[i][random_index_2]
    #             mutants[i][random_index_2] = val

            
    #     return mutants 


    #endregion