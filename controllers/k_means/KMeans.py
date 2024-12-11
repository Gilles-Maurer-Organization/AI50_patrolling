import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from KMeans_AG import AlgorithmeGenetique as AG

class KMeans:
    def __init__(self, nb_agents, list_points):
        self.nb_clusters = nb_agents  
        self.list_points = list_points  
        self.centers = None  
        self.clusters = {}  


    def launch(self, activePlot=False):
        """
        Launch a KMeans algorithm to create cluster and the connect point in the same cluster using an genetic algorithm
        Args:
           activePlot (bool) : activate or not plot which show results, can be used to see detail of both algorithms 
        Returns:
            result (list of list of int) : path found for each agent
        """
        # Set activePlot 
        self.activePlot = activePlot

        # Run KMean algorithm to group the points
        self.group_points() 
        # Run genetic algorithm to connect the points in the same cluster
        result = self.connect_points()

        print(np.sum(result[1]))
        
        return result[0]


    def group_points(self): 
        """
        Create one cluster by agent and optimize the attribution of each point in a cluster following KMeans algorithm
        """
        self.initialize_centers()
        prev_centers = np.empty_like(self.centers)
        
        # Loop until convergence
        while not np.allclose(self.centers, prev_centers):  
            prev_centers = self.centers.copy()
            
            # Compute distance matrix betwenn all points and all centers
            distances = cdist(self.list_points, self.centers)
            
            # Assign each point to the closest centers
            clusters = np.argmin(distances, axis=1)
            
            # Replace each center in the center of his cluster
            self.actualize_centers(clusters)

        if self.activePlot:
            self.plot(clusters)


    def initialize_centers(self): 
        """
        Initialize all center randomly by taking for each the coordinates of a random point in the list
        """
        self.centers = self.list_points[np.random.choice(len(self.list_points), self.nb_clusters, replace=False)]


    def actualize_centers(self, clusters): 
        """
        Replace each center on the mean position of his cluster and actualize the list of cluster in attribute
        Args:
           clusters (list of int) : associate the number of his cluster for each point 
           e.g. : [0, 2, 0, 1] -> points 0 and 2 in cluster 0 ; points 3 in cluster 1 ; point 1 in cluster 2   
        """
        for i in range(self.nb_clusters):

            # Take all points in the center i 
            cluster = self.list_points[clusters == i]
            
            # Actualise the list of cluster 
            self.clusters[i] = cluster

            # If there is at least 1 point in the cluster we 
            if len(cluster) > 0:
                self.centers[i] = np.mean(cluster, axis=0)


    def plot(self, clusters):
        """
        Display all the point with a color for each cluster and put a star to mark the position of the centers
        Args:
           clusters (list of int) : associate the number of his cluster for each point 
           e.g. : [0, 2, 0, 1] -> points 0 and 2 in cluster 0 ; points 3 in cluster 1 ; point 1 in cluster 2   
        """
        # Define a list of colors for the clusters
        colors = ['red', 'blue', 'green', 'purple', 'orange']  
        
        ax = plt.subplots()[1]

        # For each cluster we draw the points in the same color
        for i in range(self.nb_clusters):
            cluster_points = self.list_points[clusters == i]
            ax.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[i % len(colors)], label=f'Cluster {i+1}')
        
        # Display the window
        ax.scatter(self.centers[:, 0], self.centers[:, 1], c='black', marker='*', s=200, label='Centers')
        ax.legend()
        ax.set_title('K-means Clustering Process')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        plt.show()


    def connect_points(self):
        """
        Run the genetic algorithm to connect each point in the same cluster  
        """
        min_sol_ag, min_cost_ag = [], []
        if self.activePlot:
            ax = plt.subplots()[1]

        # For each cluster
        for i in range(len(self.clusters)):
            
            list_points = self.clusters[i]

            # Compute the distance between each points
            distances = cdist(list_points, list_points)

            # Run the genetic algorithm to connect the points
            ag = AG(list_points, distances)
            result = ag.run()

            # Append the result to the list of all results
            min_sol_ag.append(result[0].tolist())
            min_cost_ag.append(result[1])

            if self.activePlot:
                ax.plot(list_points[result[0], 0], list_points[result[0], 1], 'o-')

        if self.activePlot:
            plt.show() 

        return min_sol_ag, min_cost_ag

if __name__ == '__main__':
    nb_agents = 5  # Nombre de clusters
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
    print(kmeans.launch(True))
    





        



        


    