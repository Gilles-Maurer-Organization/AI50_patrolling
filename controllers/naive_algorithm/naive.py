import numpy as np
import random as rd

class Naive:
    def __init__(self,nb_agent,distance_matrix):
        self.nb_agent = nb_agent
        self.distance_matrix = distance_matrix
        pass
    
    
    def naive_shortest_path(self):
        
        nb_nodes = self.distance_matrix.shape[0]
        visited = [False] * nb_nodes
        path = []

        # Commencer à partir du nœud 0 (ou n'importe quel autre nœud)
        current_node = rd.randint(0,nb_nodes-1)
        path.append(current_node)
        visited[current_node] = True
        
        while len(path) < nb_nodes:
            # Trouver le nœud le plus proche non visité
            next_node = np.argmin([self.distance_matrix[current_node][i] if not visited[i] else np.inf for i in range(nb_nodes)])
            path.append(next_node)
            visited[next_node] = True
            current_node = next_node

        path.append(path[0])
        
        return path
        
    
    def launch(self):

        paths = []
        #a partir d'un graphe et du nombre d'agents
        #génére un chemin le plus court passant par tous les points et ne se répète pas

        path = self.naive_shortest_path()

        #Rajouter les noeuds relier chacun des neouds du indicatif path
        

        if(self.nb_agent > 1):
            for idx in range(self.nb_agent):
                agent_start_index = int(len(path)/self.nb_agent)
                paths.append(path.copy())
                for i in range(agent_start_index):
                    path.append(path[0])
                    path.pop(0)
        else :
            paths.append(path.copy())
        
        #retourne la liste des chemins de chaque agent
        return path,paths
    


def main():
    nb_agent = 1

    coords = np.array([
        [0, 0],  
        [0, 1],  
        [1, 1],  
        [1, 2],   
        [1, 3],  
        [1, 5],
        [6, 1],
        [3, 0]
    ])

    # Calculer la matrice de distances
    nb_nodes = len(coords)
    distance_matrix = np.zeros((nb_nodes, nb_nodes))
    for i in range(nb_nodes):
        for j in range(nb_nodes):
            distance_matrix[i][j] = np.linalg.norm(coords[i] - coords[j])  # Distance euclidienne
    
    #Matrice de liens entre chaque noeuds 
    
    naif = Naive(nb_agent,distance_matrix)
    path,paths = naif.launch()
    print("Le chemin à parcourir : ", path)
    print("Les chemins de chaque agent : ", paths)



if __name__ == "__main__":
    
    main()
    