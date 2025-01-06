class Node:
    """
    This class represents a 2D node point with x and y coordinates.

    It allows for getting and setting the coordinates with type checks
    for validation.
    
    Attributes:
        _x (int): The x-coordinate of the node.
        _y (int): The y-coordinate of the node.
    """
    def __init__(self, x: int, y: int, idleness: int = 0) -> None:
        self._x = x
        self._y = y
        self._idleness = idleness

    @property
    def x(self) -> int:
        """
        Getter for the x-coordinate.

        Returns:
            int: The x-coordinate of the point.
        """
        return self._x
    
    @property
    def y(self) -> int:
        """
        Getter for the y-coordinate.

        Returns:
            int: The y-coordinate of the point.
        """
        return self._y
    
    @property
    def idleness(self) -> int:
        """
        Getter for the idleness.

        Returns:
            idleness: The idleness of the point.
        """
        return self._idleness
        
    
    @property
    def idleness(self) -> int:
        """
        Getter for the idleness.

        Returns:
            idleness: The idleness of the point.
        """
        return self._idleness
        
    
    @x.setter
    def x(self, new_x: int) -> None:
        """
        Setter for the x-coordinate.
        This method ensures the new value is an integer.
        
        Args:
            new_x (int): The new x-coordinate to set.
        
        Raises:
            ValueError: If the provided value is not an integer.
        """
        if not isinstance(new_x, int):
            raise ValueError("new x must be an int value.")
        self._x = new_x
    
    @y.setter
    def y(self, new_y: int) -> None:
        """
        Setter for the y-coordinate.
        This method ensures the new value is an integer.
        
        Args:
            new_y (int): The new y-coordinate to set.
        
        Raises:
            ValueError: If the provided value is not an integer.
        """
        if not isinstance(new_y, int):
            raise ValueError("new y must be an int value.")
        self._y = new_y

    @idleness.setter
    def idleness(self, new_idleness: int) -> None:
        """
        Setter for the idleness.
        This method ensures the new value is an integer.
        
        Args:
            new_idleness (int): The new idleness to set.
        
        Raises:
            ValueError: If the provided value is not an integer.
        """
        if not isinstance(new_idleness, int):
            raise ValueError("new idleness must be an int value.")
        self._idleness = new_idleness