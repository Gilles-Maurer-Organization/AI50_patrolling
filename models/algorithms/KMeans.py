from models.algorithms.IAlgorithmModel import IAlgorithmModel

class KMeans(IAlgorithmModel):
    """
    The KMeans class implements the K-means clustering algorithm.
    It inherits from the IAlgorithmModel interface and provides
    specific parameters for the K-means algorithm.
    
    Attributes:
        _parameters (dict): A dictionary to store the parameters of the
            K-means algorithm.
        _name (str): The name of the algorithm.
    """
    def __init__(self) -> None:
        self._parameters = {}

        self._name = "K-means"
    
    @property
    def parameters(self) -> None:
        """
        Returns the parameters for the K-means algorithm.
        
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
            str: The name of the algorithm, "K-means".
        """
        return self._name