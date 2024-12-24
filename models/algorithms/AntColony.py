from models.Graph import Graph
from models.TextBox import TextBox
from models.algorithms.IAlgorithmModel import IAlgorithmModel
from services.algorithms.AntColonyAlgorithm import AntColonyAlgorithm
from services.algorithms.IAlgorithm import IAlgorithm

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
        beta=4,
        q=100,
        evaporation=0.1,
        nb_colony = 5
    ) -> None:
        self._parameters = {
            "Alpha": TextBox(str(alpha)),
            "Beta": TextBox(str(beta)),
            "Evaporation rate": TextBox(str(evaporation)),
            "Pheromone quantity": TextBox(str(q)),
            "Nb colony" : TextBox(str(nb_colony)),
            "Nb iterations": TextBox(str(nb_iterations)),
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
    
    def initialize_algorithm(
            self,
            nb_agents : int,
            graph : Graph
        ) -> IAlgorithm :
        """
        Initializes the Ant Colony algorithm with the given parameters.
        
        Args:
            nb_agents (int): The number of agents to use in the algorithm.
            graph (Graph): The graph on which the algorithm will be applied.
        
        Returns:
            AntColonyAlgorithm: An instance of the AntColonyAlgorithm
            class initialized with the given parameters.
        """
        return AntColonyAlgorithm(self._parameters, nb_agents, graph)