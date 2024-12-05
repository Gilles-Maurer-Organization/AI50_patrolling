from abc import ABC, abstractmethod

class IAlgorithm(ABC):
    """
    This interface owns an abstract method that must be implemented by
    the related algorithms.
    """
    @abstractmethod
    def launch(self):
        """
        Launches the related algorithm in order to find the best paths.
        """
        pass