class CheckBox:
    """
    Represents a checkbox with an enabled/disabled state.

    Attributes:
        _enabled (bool): The current state of the checkbox
            (True for enabled, False for disabled).
    """
    def __init__(self):
        self._enabled = False

    @property
    def enabled(self) -> bool:
        """
        Returns the current state of the checkbox.

        Returns:
            bool: True if the checkbox is enabled, False if it is disabled.
        """
        return self._enabled

    def toggle(self) -> None:
        """
        Toggles the checkbox state between enabled and disabled.
        """
        self._enabled = not self._enabled