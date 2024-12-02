from models.algorithms.IAlgorithmModel import IAlgorithmModel
from models.TextBox import TextBox

class Evolutional(IAlgorithmModel):
    """
    This class implements an Evolutionary Algorithm.
    It inherits from the IAlgorithmModel interface and provides specific
    parameters for the Evolutional algorithm.
    
    Attributes:
        _parameters (dict): A dictionary storing the algorithm parameters, each wrapped in a TextBox object.
        _name (str): The name of the algorithm, "Evolutional Algorithm".
    
    Methods:
        parameters:
            Returns the dictionary of parameters for the Evolutional algorithm.
        
        name:
            Returns the name of the algorithm.
    """
    def __init__(self, nb_iterations: int = 100, population_size: int = 10, nb_individuals: int = 10):
        self._parameters = {
            "Number of iterations": TextBox(str(nb_iterations)),
            "Population size": TextBox(str(population_size)),
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