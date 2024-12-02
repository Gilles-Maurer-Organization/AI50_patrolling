from models.algorithms.IAlgorithmModel import IAlgorithmModel

class Naive(IAlgorithmModel):
    """
    The Naive class implements a naive algorithm.
    It inherits from the IAlgorithmModel interface and provides the 
    basic parameters and name for the algorithm.
    
    Attributes:
        _parameters (dict): A dictionary to store the parameters for the naive algorithm.
        _name (str): The name of the algorithm, "Naive Algorithm".
    
    Methods:
        parameters:
            Returns the dictionary of parameters for the naive algorithm.
        
        name:
            Returns the name of the algorithm.
    """
    def __init__(self):
        self._parameters = {}
        self._name = "Naive Algorithm"
    
    @property
    def parameters(self) -> None:
        """
        Returns the parameters for the Naive algorithm.
        
        Returns:
            dict: A dictionary containing the parameters of the algorithm.
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