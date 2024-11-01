class Button:
    def __init__(self, text: str, action: callable = None, enabled = True) -> None:
        self.text = text
        self.action = action
        self.enabled = enabled

    def click(self) -> None:
        '''
        Cette méthode exécute l'action associée au bouton si celle-ci est définie.
        
        Cette méthode est appelée lorsque le bouton est cliqué.
        '''
        if self.action:
            self.action()

    def is_enabled(self) -> bool:
        return self.enabled

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled
