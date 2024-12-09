import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from KMeans_AG import AlgorithmeGenetique as AG

class KMeans:
    def __init__(self, nb_agents, list_points):
        self.nb_agents = nb_agents  # Nombre de clusters
        self.list_points = list_points  # Points à classer
        self.centers = None  # Centres des clusters
        self.groups = {}  # Points assignés à chaque cluster


    def launch(self, visualize=False):

        self.kmeans(visualize) 
        
        # Afficher les centres finaux
        print("Final centers: ", self.centers)

        result = self.connect_points(visualize)
        return result

    def kmeans(self, visualize): 
        # Initialiser les centres au hasard parmi les points existants
        self.centers = self.list_points[np.random.choice(len(self.list_points), self.nb_agents, replace=False)]
        prev_centers = np.zeros_like(self.centers)
        
        if visualize:
            plt.ion()  # Mode interactif pour mettre à jour le graphique
            ax = plt.subplots()[1]

        while not np.allclose(self.centers, prev_centers):  # Boucler jusqu'à convergence
            prev_centers = self.centers.copy()
            
            # Calculer les distances entre les points et les centres
            distances = cdist(self.list_points, self.centers)
            
            # Assigner chaque point au centre le plus proche
            clusters = np.argmin(distances, axis=1)
            
            # Recalculer les centres en prenant la moyenne des points assignés
            for i in range(self.nb_agents):
                cluster_points = self.list_points[clusters == i]
                self.groups[i] = cluster_points
                if len(cluster_points) > 0:
                    self.centers[i] = np.mean(cluster_points, axis=0)

                                # Visualisation du processus
            if visualize:
                ax.clear()
                self._plot(ax, clusters)
                plt.pause(0.5)  # Pause pour visualiser chaque étape

        if visualize:
            plt.ioff()  # Désactiver le mode interactif
            plt.show()  # Garder le dernier graphique affiché

    def _plot(self, ax, clusters):
        """Affiche les points, les clusters et les centres."""
        colors = ['red', 'blue', 'green', 'purple', 'orange']  # Différentes couleurs pour les clusters
        
        for i in range(self.nb_agents):
            cluster_points = self.list_points[clusters == i]
            ax.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[i % len(colors)], label=f'Cluster {i+1}')
        
        # Afficher les centres
        ax.scatter(self.centers[:, 0], self.centers[:, 1], c='black', marker='*', s=200, label='Centers')
        ax.legend()
        ax.set_title('K-means Clustering Process')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')


    def connect_points(self, visualize):

        min_sol_ag, cout_min_ag = [], []
        if visualize:
            ax = plt.subplots()[1]

        # Afficher les chemins de chaque cluster
        for i in range(nb_agents):
            
            list_points = self.groups[i]
            distances = cdist(list_points, list_points)

            ag = AG(list_points, distances)
            result = ag.run()

            min_sol_ag.append(result[0].tolist())
            cout_min_ag.append(result[1])

            if visualize:
                ax.plot(list_points[result[0], 0], list_points[result[0], 1], 'o-')

        if visualize:
            plt.show() 


        return min_sol_ag

if __name__ == '__main__':
    nb_agents = 3  # Nombre de clusters
    list_points = np.array([
    # Cluster 1
    [1, 2], [2, 1], [1, 1], [2, 2], [3, 1], [1.5, 1.8], [2.2, 2.1], [0.8, 1.9],
    # Cluster 2
    [8, 8], [9, 9], [7, 8], [8.5, 8.5], [9.1, 8.7], [7.5, 9], [8.8, 7.8],
    # Cluster 3
    [12, 14], [13, 15], [12.5, 13.5], [13.1, 14.8], [12.8, 14.2], [12.2, 13.9],
    # Cluster 4
    [20, 22], [21, 23], [20.5, 21.5], [21.2, 22.8], [20.8, 21.9], [20.1, 22.5],
    # Cluster 5
    [30, 30], [31, 31], [29, 29], [30.5, 30.2], [30.8, 30.9], [29.5, 29.5],
    # Cluster 6 (noisy data, scattered points)
    [5, 15], [16, 20], [10, 25], [14, 18], [3, 22], [8, 12], [25, 5], [19, 13],
    ])# Points à classer
    
    # Initialiser et exécuter l'algorithme K-means
    kmeans = KMeans(nb_agents, list_points)
    print(kmeans.launch())
    





        



        


    