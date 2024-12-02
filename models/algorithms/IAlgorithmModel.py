from abc import ABC, abstractmethod

class IAlgorithmModel(ABC):
    @property
    @abstractmethod
    def parameters(self) -> None:
        """
        Returns the parameters of the algorithm.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> None:
        """
        Returns the name of the algorithm.
        """
        pass