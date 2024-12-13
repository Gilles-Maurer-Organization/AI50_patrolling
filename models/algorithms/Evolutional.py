from models.algorithms.IAlgorithmModel import IAlgorithmModel
from models.TextBox import TextBox
from services.algorithms import EvolutionalAlgorithm

class Evolutional(IAlgorithmModel):
    """
    This class implements an Evolutionary Algorithm.
    It inherits from the IAlgorithmModel interface and provides
    specific parameters for the Evolutional algorithm.
    
    Attributes:
        _parameters (dict): A dictionary storing the algorithm
            parameters, each wrapped in a TextBox object.
        _name (str): The name of the algorithm.
    """
    def __init__(
        self,
        nb_iterations: int = 100,
        nb_individuals: int = 10
    ) -> None:
        self._parameters = {
            "Number of iterations": TextBox(str(nb_iterations)),
            "Number of individuals": TextBox(str(nb_individuals))
        }

        self._name = "Evolutional Algorithm"

    @property
    def parameters(self) -> None:
        """
        Returns the parameters for the Evolutional algorithm.
        
        Returns:
            dict: A dictionary containing the algorithm parameters.
        """
        return self._parameters
    
    @property
    def name(self) -> None:
        """
        Returns the name of the algorithm.
        
        Returns:
            str: The name of the algorithm, "Evolutional Algorithm".
        """
        return self._name
    
     
    def initialize_algorithm(self, nb_agents, complete_adjacency_matrix) -> None :
        return EvolutionalAlgorithm(self._parameters, nb_agents, complete_adjacency_matrix)