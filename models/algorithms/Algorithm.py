from abc import ABC, abstractmethod

class Algorithm:
    def __init__(self) -> None:
        '''
        This class is abstract and and serves as a base for other classes.
        It doesn't have methods to implement but can be used to indicate a
        type of algorithm object
        '''
        super().__init__()
