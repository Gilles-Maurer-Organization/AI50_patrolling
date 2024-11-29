from abc import ABC, abstractmethod

class IAlgorithm(ABC):

    @abstractmethod
    def launch(self):
        pass