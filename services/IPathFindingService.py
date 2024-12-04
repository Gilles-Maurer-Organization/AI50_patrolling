from abc import ABC, abstractmethod

class IPathFindingService(ABC):
    """
    This interface owns an abstract method that must be implemented by
    the related services.
    """
    @abstractmethod
    def find_path(self):
        """
        Finds the shortest path between two nodes.
        """
        pass