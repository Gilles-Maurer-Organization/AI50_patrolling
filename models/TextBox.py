class TextBox:
    def __init__(self, default_text=""):
        self.active = False
        self.first_input = True
        self.text_content = default_text
        self.default_text = default_text

    def reset(self):
        """
        Cette méthode réinitialise la zone de texte à son texte par défaut.
        """
        self.text_content = self.default_text
        self.first_input = True

    def add_character(self, char):
        """
        Cette méthode ajoute un caractère à la zone de texte, en remplaçant le texte par défaut si nécessaire.
        """
        if self.first_input:
            self.text_content = ""
            self.first_input = False
        self.text_content += char

    def handle_backspace(self):
        """
        Cette méthode gère la touche Backspace et réinitialise le texte si vide.
        """
        if self.default_text != self.text_content:
            self.remove_character()
            if self.is_empty():
                self.reset()

    def remove_character(self):
        """
        Cette méthode supprime le dernier caractère de la zone de texte.
        """
        self.text_content = self.text_content[:-1]

    def is_empty(self):
        """
        Cette méthode vérifie si la zone de texte est vide.
        """
        return len(self.text_content) == 0
    
    def is_default_text(self):
        '''
        Cette méthode retourne vrai dans le cas où le texte initial est identique au texte actuel
        '''
        return self.default_text == self.text_content