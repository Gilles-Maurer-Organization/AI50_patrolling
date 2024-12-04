class Node:
    """
    This class represents a 2D node point with x and y coordinates.

    It allows for getting and setting the coordinates with type checks
    for validation.
    
    Attributes:
        _x (int): The x-coordinate of the node.
        _y (int): The y-coordinate of the node.
    """
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

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