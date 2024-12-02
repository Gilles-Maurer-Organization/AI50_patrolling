from models.algorithms.IAlgorithmModel import IAlgorithmModel

class ScrollingList:
    """
    This class manages a list of algorithms and tracks the selected algorithm.
    
    Attributes:
        _active (bool): A flag indicating whether the list is active or not.
        _algorithms (list[IAlgorithmModel]): A list of algorithm models.
        _selected_algorithm (IAlgorithmModel | None): The currently selected algorithm.
    
    Methods:
        active:
            Getter and setter for the 'active' attribute.
        
        algorithms:
            Getter for the 'algorithms' attribute.
        
        selected_algorithm:
            Getter and setter for the 'selected_algorithm' attribute.
        
        has_an_algorithm_selected:
            Returns a boolean indicating whether a selection has been made.
    """
    def __init__(self, algorithms: list[IAlgorithmModel]) -> None:
        self._active = False
        self._algorithms = algorithms
        self._selected_algorithm = None

    @property
    def algorithms(self) -> list[IAlgorithmModel]:
        """
        Getter for the 'algorithms' attribute.
        
        Returns:
            list[IAlgorithmModel]: The list of algorithm models.
        """
        return self._algorithms
    
    @property
    def selected_algorithm(self) -> IAlgorithmModel:
        """
        Getter for the 'selected_algorithm' attribute.
        
        Returns:
            IAlgorithmModel | None: The currently selected algorithm.
        """
        return self._selected_algorithm
    
    @selected_algorithm.setter
    def selected_algorithm(self, algorithm: IAlgorithmModel) -> None:
        """
        Setter for the 'selected_algorithm' attribute.
        
        Args:
            algorithm (IAlgorithmModel): The new algorithm to be selected.
        """
        if not isinstance(algorithm, IAlgorithmModel):
            raise ValueError("Selected algorithm must be an instance of IAlgorithmModel.")
        self._selected_algorithm = algorithm
    
    def has_an_algorithm_selected(self) -> bool:
        """
        Returns a boolean indicating whether a selection has been made.
        
        Returns:
            bool: Whether an algorithm is selected.
        """
        return self.selected_algorithm is not None