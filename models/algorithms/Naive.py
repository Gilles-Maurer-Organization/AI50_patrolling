from models.Graph import Graph
from models.algorithms.IAlgorithmModel import IAlgorithmModel
from services.algorithms.IAlgorithm import IAlgorithm
from services.algorithms.NaiveAlgorithm import NaiveAlgorithm
class Naive(IAlgorithmModel):
    """
    The Naive class implements a naive algorithm.

    It inherits from the IAlgorithmModel interface and provides the 
    basic parameters and name for the algorithm.
    
    Attributes:
        _parameters (dict): A dictionary to store the parameters for
            the naive algorithm.
        _name (str): The name of the algorithm, "Naive Algorithm".
    """
    def __init__(self):
        self._parameters = {}
        self._name = "Naive Algorithm"
    
    @property
    def parameters(self) -> None:
        """
        Returns the parameters for the Naive algorithm.
        
        Returns:
            dict: A dictionary containing the parameters of the
                algorithm.
        """
        return self._parameters
    
    @property
    def name(self) -> None:
        """
        Returns the name of the algorithm.
        
        Returns:
            str: The name of the algorithm, "Naive Algorithm".
        """
        return self._name
    
    def initialize_algorithm(
            self,
            nb_agents : int,
            graph : Graph
        ) -> IAlgorithm :
        """
        Initializes the Naive Algorithm with the given parameters.
        
        Args:
            nb_agents (int): The number of agents to use in the algorithm.
            graph (Graph): The graph on which the algorithm will be applied.
        
        Returns:
            NaiveAlgorithm: An instance of the NaiveAlgorithm
            class initialized with the given parameters.
        """
        return NaiveAlgorithm(nb_agents, graph)