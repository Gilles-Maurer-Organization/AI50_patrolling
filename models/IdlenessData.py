import numpy as np

from models.Node import Node

class IdlenessData:

    """
    this class contains the Data associated to the idleness 
    during runtime.

    Attributes:
        _average_idleness: the average idleness during the simulation
        _max_idleness: the maximal idleness during the simulation
        _all_time_highest_idleness : the all-time highest idleness of the simulation
          
    """
    
    def __init__(self) -> None:
        self._average_idleness = 0
        self._max_idleness = 0
        self._all_time_highest_idleness = 0

    def reset(self) -> None:
        """
        Resets all idleness-related data to their initial state.
        """
        self._average_idleness = 0
        self._max_idleness = 0
        self._all_time_highest_idleness = 0
        
    def get_idleness_data(self) -> tuple[float, float, float] :
        """
        returns the data (average, max and a-t highest idleness).
        """
        return self._average_idleness, self._max_idleness, self._all_time_highest_idleness
    

    def update_idleness(self,graph_nodes : list[Node]) -> None:
        """
        updates the idleness values using a dedicated function.
        """
        self._compute_idleness_values(graph_nodes)

    def _compute_idleness_values(self, graph_nodes : list[Node]) -> None:
        """
        Computes the average idleness of the current simulation.
        Computes the highest idleness of the current simulation.
        Computes the all-time highest idleness of the simulation.

        """

        idleness_values = []

        #retrieving all the idleness's in a list
        for node in graph_nodes:
           idleness_values.append(node.idleness)
           
        #computing mean value of the list
        average_id = np.mean(idleness_values)

        #retrieving the max idleness
        max_id = np.max(idleness_values)

        #check if there is a new all-time highest value
        if max_id > self._all_time_highest_idleness:
            self._all_time_highest_idleness = max_id

        #inserting it into the corresponding attributes
        self._average_idleness = average_id  
        self._max_idleness = max_id          
