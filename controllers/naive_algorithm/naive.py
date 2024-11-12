import numpy as np
import random as rd

class Naive:
    def __init__(self):
        pass
    
    
    def naive_shortest_path(self,distance_matrix):
        
        nb_nodes = distance_matrix.shape[0]
        visited = [False] * nb_nodes
        path = []
        
        #Ajouter le test pour s'executer tant que le chemin ne respecte pas les liens entre les noeuds (car il ne passe pas par le même noeud)

        # Commencer à partir du nœud 0 (ou n'importe quel autre nœud)
        current_node = rd.randint(0,nb_nodes-1)
        path.append(current_node)
        visited[current_node] = True
        
        while len(path) < nb_nodes:
            # Trouver le nœud le plus proche non visité
            next_node = np.argmin([distance_matrix[current_node][i] if not visited[i] else np.inf for i in range(nb_nodes)])
            path.append(next_node)
            visited[next_node] = True
            current_node = next_node

        
        return path
        
    
    def launch(self,nb_agents,distance_matrix):

        paths = []
        #a partir d'un graphe et du nombre d'agents
        #génére un chemin le plus court passant par tous les points et ne se répète pas

        path = self.naive_shortest_path(distance_matrix)

        for idx in range(nb_agents):
            agent_start_index = int(len(path)/nb_agents)
            paths.append(path.copy())
            for i in range(agent_start_index):
                path.append(path[0])
                path.pop(0)
        
        #retourne la liste des chemins de chaque agent
        return path,paths
    


def main():
    
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
    
    
    
    naif = Naive()
    
    path,paths = naif.launch(4,distance_matrix)
    print(path)
    print(paths)



if __name__ == "__main__":
    
    main()
    