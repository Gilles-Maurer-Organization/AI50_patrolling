class TextBox:
    """
    A class that represents a text box with functionalities for handling text input and state.
    
    Attributes:
        _active (bool): A flag to indicate if the text box is active.
        _first_input (bool): A flag to track if it is the first input.
        _text_content (str): The content of the text box.
        _default_text (str): The default text of the text box.
    
    Methods:
        active: Getter and setter for the active attribute.
        text_content: Getter and setter for the text content.
        default_text: Getter for the default text.
        first_input: Getter for the first input boolean.
        empty: Returns a boolean indicating if the text content is empty.
        default_text: Returns a boolean indicating if the text content matches the default text.
        filled: Returns a boolean indicating if the text content is not empty and differs from the default text.
        reset: Resets the text box to its default text.
        add_character: Adds a character to the text content.
        handle_backspace: Handles the backspace functionality for text removal.
        remove_character: Removes the last character from the text content.
    """
    def __init__(self, default_text=""):
        self._active = False
        self._first_input = True
        self._text_content = default_text
        self._default_text = default_text

    @property
    def active(self) -> bool:
        """
        Getter for the active attribute.
        
        Returns:
            bool: Whether the text box is active.
        """
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        """
        Sets the text box to active.
        
        Args:
            active (bool): The new value for the active attribute.
        """
        self._active = active

    @property
    def text_content(self) -> str:
        """
        Getter for the text content of the text box.
        
        Returns:
            str: The current text content of the text box.
        """
        return self._text_content

    @text_content.setter
    def text_content(self, text: str) -> None:
        """
        Sets the text content of the text box.
        
        Args:
            text (str): The new text to set for the text box.
        """
        self._text_content = text

    @property
    def default_text(self) -> str:
        """
        Getter for the default text.
        
        Returns:
            str: The default text of the text box.
        """
        return self._default_text
    
    @property
    def first_input(self) -> bool:
        """
        Getter for the _first_input attribute.
        
        This property returns whether the text box is in its first input state,
        which is used to determine if the text content is still the default text.
        
        Returns:
            bool: True if it's the first input, False otherwise.
        """
        return self._first_input
    
    @property
    def empty(self) -> bool:
        """
        Returns a boolean indicating if the text content is empty.
        
        Returns:
            bool: Whether the text content is empty.
        """
        return len(self._text_content) == 0
    
    @property
    def filled(self) -> bool:
        """
        Returns a boolean indicating if the text content is not empty and differs from the default text.
        
        Returns:
            bool: Whether the text content is filled and differs from the default text.
        """
        return self._default_text != self._text_content and not self.empty
    
    def reset(self) -> None:
        """
        Resets the text box to its default text.
        """
        self._text_content = self._default_text
        self._first_input = True

    def add_character(self, char) -> None:
        """
        Adds a character to the text content, replacing the default text if necessary.
        
        Args:
            char (str): The character to add to the text content.
        """
        if self._first_input:
            self._text_content = ""
            self._first_input = False
        self._text_content += char

    def handle_backspace(self) -> None:
        """
        Handles the backspace functionality and resets the text if it becomes empty.
        """
        if self._default_text != self._text_content:
            self.remove_character()
            if self.empty:
                self.reset()

    def remove_character(self) -> None:
        """
        Removes the last character from the text content.
        """
        self._text_content = self._text_content[:-1]