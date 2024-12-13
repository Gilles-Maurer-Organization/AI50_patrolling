from models.TextBox import TextBox
from models.algorithms.IAlgorithmModel import IAlgorithmModel
from services.algorithms.AntColonyAlgorithm import AntColonyAlgorithm

class AntColony(IAlgorithmModel):
    """
    This class implements the Ant Colony Optimization algorithm.
    It inherits from the IAlgorithmModel interface and provides
    specific parameters for the Ant Colony algorithm.
    
    Attributes:
        _parameters (dict): A dictionary storing the algorithm
            parameters, each wrapped in a TextBox object.
        _name (str): The name of the algorithm.
    """
    def __init__(
        self,
        nb_iterations=100,
        alpha=1,
        beta=1,
        q=10,
        evaporation=0.5,
        nb_colony = 3
    ) -> None:
        self._parameters = {
            "Alpha": TextBox(str(alpha)),
            "Beta": TextBox(str(beta)),
            "Pheromone quantity": TextBox(str(q)),
            "Nb colony" : TextBox(str(nb_colony)),
            "Nb iterations": TextBox(str(nb_iterations)),
            "Evaporation rate": TextBox(str(evaporation))
        }
        self._name = "Ant Colony Algorithm"

    @property
    def parameters(self) -> None:
        """
        Returns the parameters for the Ant Colony algorithm.
        
        Returns:
            dict: A dictionary containing the algorithm parameters.
        """
        return self._parameters
    
    @property
    def name(self) -> None:
        """
        Returns the name of the algorithm.
        
        Returns:
            str: The name of the algorithm, "Ant Colony Algorithm".
        """
        return self._name
    
    def initialize_algorithm(self, nb_agents, complete_adjacency_matrix) -> None :
        return AntColonyAlgorithm(self._parameters, nb_agents, complete_adjacency_matrix)