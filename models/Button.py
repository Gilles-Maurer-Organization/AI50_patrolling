class Button:
    def __init__(self, text: str, action: callable = None) -> None:
        self.text = text
        self.action = action

    def click(self) -> None:
        '''
        Cette méthode exécute l'action associée au bouton si celle-ci est définie.
        
        Cette méthode est appelée lorsque le bouton est cliqué.
        '''
        if self.action:
            self.action()
