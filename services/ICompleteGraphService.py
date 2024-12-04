from abc import ABC, abstractmethod

class ICompleteGraphService(ABC):
    """
    This interface owns an abstract method that must be implemented by
    the related services.
    """
    @abstractmethod
    def create_complete_graph(self) -> None:
        """
        Creates the complete graph thanks to a specific algorithm.
        """
        pass

    @property
    @abstractmethod
    def complete_graph(self) -> list[list[float]]:
        """
        Returns the complete graph.
        """
        pass