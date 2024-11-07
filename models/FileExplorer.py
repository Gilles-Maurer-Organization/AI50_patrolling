class FileExplorer:
    def __init__(self):
        self.path_selected = None
        self.opened = False
    
    def is_opened(self) -> bool:
        return self.opened

    def set_is_opened(self, opened) -> None:
        self.opened = opened

    def get_path(self) -> str:
        return self.path_selected

    def set_path(self, path: str) -> None:
        self.path_selected = path