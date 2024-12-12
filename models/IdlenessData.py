
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

        nodes_idleness_list: list containing the idleness of each node
          
    """
    
    def __init__(self,nodes_list : list[Node]) -> Node:

        self.average_idleness = 0
        self.max_idleness = 0
        self.graph_nodes = nodes_list

        self.data = {
            "Current average Idleness": self.average_idleness,
            "Current maximal Idleness": self.max_idleness,
        }
    
    
    def get_idleness_data(self) -> None:
        """
        Gets the data (average and max idleness)
        """
        return self.data
    
    #called from the controller ???? 
    def update_idleness(self) -> None:
        """
        updates the idleness values using a dedicated function.

        """
        self.compute_idleness_values()

    def compute_idleness_values(self) -> None:
        """
        Computes the average idleness of the current simulation.
        """

        idleness_values = [1,2,3,4,5]
        #retrieving all the idleness's in a list
        #for node in self.graph_nodes:
        #    idleness_values.append(node.idleness)

        #computing mean value of the list
        average_id = np.mean(idleness_values)

        #retrieving the max idleness
        max_id = np.max(idleness_values)

        #inserting it into the corresponding attribute
        self.average_idleness = average_id  #2.5
        self.max_idleness = max_id          #5


    