class FileExplorer:
    '''
    This class represents a file explorer that manages the state of file selection and whether the file explorer is opened.

    Attributes:
        path_selected (str or None): The path of the selected file, initially None if no file is selected.
        opened (bool): The state of the file explorer, indicating whether it is opened or closed.

    Methods:
        is_opened() -> bool:
            Returns whether the file explorer is currently opened.
        
        set_is_opened(opened: bool) -> None:
            Sets the state of the file explorer (opened or closed).
        
        get_path() -> str:
            Returns the path of the selected file.
        
        set_path(path: str) -> None:
            Sets the path of the selected file.
    '''
    def __init__(self):
        # Initially no file is selected
        self.path_selected = None
        # Initially, the file explorer is closed
        self.opened = False 
    
    def is_opened(self) -> bool:
        '''
        This method returns if the file explorer is currently opened.
        
        Returns:
            bool: True if the file explorer is opened, False otherwise.
        '''
        return self.opened

    def set_is_opened(self, opened) -> None:
        '''
        This method sets the state of the file explorer (opened or closed).
        
        Args:
            opened (bool): The new state of the file explorer. True for opened, False for closed.
        '''
        self.opened = opened

    def get_path(self) -> str:
        '''
        This method returns the path of the selected file.
        
        Returns:
            str: The path of the selected file. If no file is selected, returns None.
        '''
        return self.path_selected

    def set_path(self, path: str) -> None:
        '''
        This method sets the path of the selected file.
        
        Args:
            path (str): The path of the file to be selected.
        '''
        self.path_selected = path