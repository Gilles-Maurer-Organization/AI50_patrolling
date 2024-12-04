class FileExplorer:
    """
    This class represents a file explorer that manages the state of
    file selection and whether the file explorer is opened.

    Attributes:
        path_selected (str or None): The path of the selected file,
            initially None if no file is selected.
        opened (bool): The state of the file explorer, indicating
            whether it is opened or closed.
    """
    def __init__(self):
        # Initially no file is selected
        self._path_selected = None
        # Initially, the file explorer is closed
        self._opened = False 
    
    @property
    def opened(self) -> bool:
        """
        Returns if the file explorer is currently opened.
        
        Returns:
            bool: True if the file explorer is opened, False otherwise.
        """
        return self._opened

    @property
    def path(self) -> str:
        """
        Returns the path of the selected file.
        
        Returns:
            str: The path of the selected file. If no file is selected,
                returns None.
        """
        return self._path_selected
    
    @opened.setter
    def opened(self, opened: bool) -> None:
        """
        Sets the state of the file explorer (opened or closed).
        
        Args:
            opened (bool): The new state of the file explorer. True for
                opened, False for closed.

        Raises:
            ValueError: If the provided value is not a boolean.
        """
        if not isinstance(opened, bool):
            raise ValueError("enabled must be a boolean value.")
        self._opened = opened

    @path.setter
    def path(self, path: str) -> None:
        """
        Sets the path of the selected file.
        
        Args:
            path (str): The path of the file to be selected.

        Raises:
            ValueError: If the provided value is not a string.
        """
        if not isinstance(path, str):
            raise ValueError("path must be a string.")
        self._path_selected = path