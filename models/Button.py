class Button:
    """
    This class represents a Button with a text label, an action, and an enabled state.
    
    Attributes:
        _text (str): The text displayed on the button.
        _action (callable): The action to execute when the button is clicked.
        _enabled (bool): The state of the button, either enabled or disabled.
    
    Methods:
        click():
            Executes the associated action when the button is clicked, if defined.
        
        enabled:
            Getter for the enabled/disabled state of the button.
        
        text:
            Getter for the text displayed on the button.
        
        action:
            Getter for the action associated with the button.
        
        enabled (setter): 
            Setter for the enabled/disabled state of the button. Raises an error if the value is not a boolean.
    """
    def __init__(self, text: str, action: callable = None, enabled = True) -> None:
        self._text = text
        self._action = action
        self._enabled = enabled

    def click(self) -> None:
        """
        Executes the action associated with the button if it is defined.

        This method is called when the button is clicked.
        """
        if self._action:
            self._action()

    @property
    def enabled(self) -> bool:
        """
        Gets the enabled state of the button.

        Returns:
            bool: True if the button is enabled, False otherwise.
        """
        return self._enabled
    
    @property
    def text(self) -> str:
        """
        Gets the text displayed on the button.

        Returns:
            str: The text of the button.
        """
        return self._text
    
    @property
    def action(self) -> str:
        """
        Gets the action associated with the button.

        Returns:
            callable: The action to be executed when the button is clicked.
        """
        return self._action

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        """
        Sets the enabled state of the button.

        Args:
            enabled (bool): The state to set for the button (True for enabled, False for disabled).
        
        Raises:
            ValueError: If the provided value is not a boolean.
        """
        if not isinstance(enabled, bool):
            raise ValueError("enabled must be a boolean value.")
        self._enabled = enabled
