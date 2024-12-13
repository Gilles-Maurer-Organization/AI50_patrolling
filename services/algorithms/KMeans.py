import numpy as np
import math
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

# from services.algorithms.IAlgorithm import IAlgorithm
from IAlgorithm import IAlgorithm
from KMeans_AG import AlgorithmeGenetique as AG

class KMeans(IAlgorithm):
    def __init__(
        self, 
        nb_agents : int, 
        list_nodes : np.ndarray[np.ndarray[float]], 
        distances : np.ndarray[np.ndarray[float]],
        nb_launch_kmeans : int, 
        activePlot : bool = False
    ) -> None:

        self._nb_clusters = nb_agents  
        self._list_nodes = list_nodes
        self._distances = distances  
        self._nb_launch_kmeans = nb_launch_kmeans
        self._activePlot = activePlot

        self._centers = None  
        self._clusters = {}  


    def launch(self) -> list[list[int]]:
        """
        Launch a KMeans algorithm to create cluster and the connect 
        node in the same cluster using an genetic algorithm.

        Args:
           activePlot (bool) : activate or not plot which show results, 
           can be used to see detail of both algorithms. 

        Returns:
            result (list of list of int) : path found for each agent.
        """
        best_result = math.inf
        best_clusters = {}

        for _ in range(self._nb_launch_kmeans):
            # Run KMean algorithm to group the nodes
            self._group_nodes() 
            result = self._evaluate_kmean()
            if result < best_result: 
                best_result = result
                best_clusters = self._clusters

        self._clusters = best_clusters

        # Run genetic algorithm to connect the nodes in the same cluster
        result = self._connect_nodes()

        return result[0]
    


    def _group_nodes(self) -> None: 
        """
        Create one cluster by agent and optimize the attribution 
        of each node in a cluster following KMeans algorithm.
        """
        self._initialize_centers()
        prev_centers = np.empty_like(self._centers)
        
        # Loop until convergence
        while not np.allclose(self._centers, prev_centers):  
            prev_centers = self._centers.copy()
            
            # Compute distance matrix betwenn all nodes and all centers
            distances = cdist(self._list_nodes, self._centers)
            
            # Assign each node to the closest centers
            clusters_attribution = np.argmin(distances, axis=1)
            
            # Replace each center in the center of his cluster
            self._actualize_centers(clusters_attribution)

        if self._activePlot:
            self._plot(clusters_attribution)


    def _initialize_centers(self) -> None: 
        """
        Initialize all center randomly by taking for each the 
        coordinates of a random node in the list.
        """
        self._centers = self._list_nodes[
            np.random.choice(len(self._list_nodes), self._nb_clusters, replace=False)
        ]


    def _actualize_centers(self, clusters_attribution : list[int]) -> None: 
        """
        Replace each center on the mean position of his cluster 
        and actualize the list of cluster in attribute.
        
        Args:
           clusters_attribution (list of int) : associate the number of 
           his cluster for each node e.g. : [0, 2, 0, 1] -> nodes 0 and 2 in cluster 0 ; 
           nodes 3 in cluster 1 ; node 1 in cluster 2.   
        """
        for i in range(self._nb_clusters):

            # Take all nodes in the center i 
            cluster = self._list_nodes[clusters_attribution == i]
            
            # Actualise the list of cluster 
            self._clusters[i] = cluster

            # If there is at least 1 node in the cluster we 
            if len(cluster) > 0:
                self._centers[i] = np.mean(cluster, axis=0)


    def _plot(self, clusters_attribution : list[int]) -> None:
        """
        Display all the node with a color for each cluster and put a 
        star to mark the position of the centers.

        Args:
           clusters_attribution (list of int) : associate the number of 
           his cluster for each node 
           e.g. : [0, 2, 0, 1] -> nodes 0 and 2 in cluster 0 ; 
           nodes 3 in cluster 1 ; node 1 in cluster 2.  
        """
        # Define a list of colors for the clusters
        colors = ['red', 'blue', 'green', 'purple', 'orange']  
        
        ax = plt.subplots()[1]

        # For each cluster we draw the nodes in the same color
        for i in range(self._nb_clusters):
            cluster_nodes = self._list_nodes[clusters_attribution == i]
            ax.scatter(
                cluster_nodes[:, 0], 
                cluster_nodes[:, 1], 
                c=colors[i % len(colors)], 
                label=f'Cluster {i+1}'
            )
        
        # Display the window
        ax.scatter(
            self._centers[:, 0], 
            self._centers[:, 1],
            c='black', 
            marker='*', 
            s=200, 
            label='Centers'
        )
        ax.legend()
        ax.set_title('K-means Clustering Process')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        plt.show()


    # calculer la somme des carrées des distances au centre
    def _evaluate_kmean(self) -> int:
        """
        Compute the sum of the squared distance between each node and 
        his center to evaluate the KMeans algorithm.
        """ 
        sum = 0
        for id_center, cluster in self._clusters.items(): 
            for node in cluster: 
                sum += self._squarred_distance(node, self._centers[id_center])

        return sum
                

    def _squarred_distance(
        self, 
        node1 : np.ndarray[float], 
        node2 : np.ndarray[float]
    ) -> float: 
        """
        Compute the squared distance between two nodes.
        """
        return ((node1[0] - node2[0]) ** 2) + ((node1[1] - node2[1]) ** 2) 


    def _connect_nodes(self) -> tuple[list[list[int]], list[float]]:
        """
        Run the genetic algorithm to connect each node in the same cluster.  
        """
        min_sol_ag, min_cost_ag = [], []
        if self._activePlot:
            ax = plt.subplots()[1]

        # For each cluster
        for i in range(len(self._clusters)):
            
            cluster = self._clusters[i]

            # Compute the distance between each nodes by using the initial distance matrix
            cluster_distances = np.empty((len(cluster), len(cluster)))

            for i in range(len(cluster)): 
                for j in range(i, len(cluster)): 
                    
                    for idx, node in enumerate(self._list_nodes):
                        if np.array_equal(node, cluster[i]):
                            id_node1 = idx
                            break

                    for idx, node in enumerate(self._list_nodes):
                        if np.array_equal(node, cluster[j]):
                            id_node2 = idx
                            break

                    cluster_distances[i][j] = self._distances[id_node1][id_node2]
                    cluster_distances[j][i] = cluster_distances[i][j]


            # Run the genetic algorithm to connect the nodes
            ag = AG(nb_nodes=len(cluster), distances=cluster_distances) 
            result = ag.run()

            # Append the result to the list of all results
            min_sol_ag.append(result[0].tolist())
            min_cost_ag.append(result[1])

            if self._activePlot:
                ax.plot(cluster[result[0], 0], cluster[result[0], 1], 'o-')

        if self._activePlot:
            plt.show() 

        return min_sol_ag, min_cost_ag


    





        



        


    