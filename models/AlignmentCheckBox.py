class AlignmentCheckBox:
    def __init__(self):
        self._alignment_enabled = False

    @property
    def alignment_enabled(self) -> bool:
        return self._alignment_enabled

    def toggle_alignment(self) -> None:
        self._alignment_enabled = not self._alignment_enabled