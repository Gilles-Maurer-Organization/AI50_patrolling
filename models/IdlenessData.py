import random as rd

import numpy as np

from models.Node import Node
from models.TextBox import TextBox

class IdlenessData:

    """
    this class contains the Data associated to the idleness 
    during runtime.

    Attributes:
        average_idleness: the average idleness during the simulation

        max_idleness: the maximal idleness during the simulation

        all_time_highest_idleness : the all-time highest idleness of the simulation

        nodes_idleness_list: list containing the idleness of each node
          
    """
    
    def __init__(self,nodes_list : list[Node]) -> Node:

        self.average_idleness = 0
        self.max_idleness = 0
        self.all_time_highest_idleness = 0
        self.graph_nodes = nodes_list
        
    def get_idleness_data(self) :
        """
        returns the data (average, max and a-t highest idleness).
        """
        return self.average_idleness, self.max_idleness, self.all_time_highest_idleness
    
    #
    def update_idleness(self) -> None:
        """
        updates the idleness values using a dedicated function.
        """
        self.compute_idleness_values()

    def compute_idleness_values(self) -> None:
        """
        Computes the average idleness of the current simulation.
        Computes the highest idleness of the current simulation.
        Computes the all-time highest idleness of the simulation.

        """

        idleness_values = [1,2,3,4,5]

        #retrieving all the idleness's in a list

        #for node in self.graph_nodes:
        #   idleness_values.append(node.idleness)
            #print(node.x,node.y)

        #at the moment, generating random values for testing
        for idx, _ in enumerate(idleness_values):
            idleness_values[idx] = round(rd.uniform(1,5000)) # NOSONAR

        #computing mean value of the list
        average_id = np.mean(idleness_values)

        #retrieving the max idleness
        max_id = np.max(idleness_values)

        #check if there is a new all-time highest value
        if max_id > self.all_time_highest_idleness:
            self.all_time_highest_idleness = max_id

        #inserting it into the corresponding attribute
        self.average_idleness = average_id  
        self.max_idleness = max_id          
