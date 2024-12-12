class AlignmentCheckBox:
    def __init__(self):
        self._alignment_enabled = False

    @property
    def alignment_enabled(self) -> bool:
        return self._alignment_enabled

    @alignment_enabled.setter
    def alignment_enabled(self, enabled) -> None:
        self._alignment_enabled = enabled