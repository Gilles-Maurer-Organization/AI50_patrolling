class ScrollingList:
    def __init__(self, text: str, algorithms: list[str]) -> None:
        self.active = False
        self.text = text
        self.algorithms = algorithms