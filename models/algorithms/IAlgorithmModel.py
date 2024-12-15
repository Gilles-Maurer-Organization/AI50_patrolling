from abc import ABC, abstractmethod

from models.Graph import Graph
from services.algorithms.IAlgorithm import IAlgorithm

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

    @abstractmethod
    def initialize_algorithm(
            self,
            nb_agents: int,
            graph: Graph
        ) -> IAlgorithm:
        pass