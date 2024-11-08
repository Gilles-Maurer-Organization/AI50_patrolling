from abc import ABC, abstractmethod

class ICompleteGraphService(ABC):
    '''
    This interface owns an abstract method that must be
    implemented by the related services.
    '''
    @abstractmethod
    def create_complete_graph(self):
        '''
        This method finds the shortest path between two nodes.
        '''
        pass