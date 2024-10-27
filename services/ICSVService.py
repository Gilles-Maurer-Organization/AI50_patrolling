from abc import ABC, abstractmethod

class ICSVService(ABC):
    @abstractmethod
    def save(self, edges_matrix, nodes_list, filename):
        pass

    @abstractmethod
    def load(self, num_file):
        pass