from enum import Enum

class Colors(Enum):
    '''
    Enumération permettant de définir les couleurs utilisés dans le programme (couleur des noeuds, couleur de sélection d'un noeud, couleur des liens, etc)
    '''
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    NODE_COLOR = (0, 100, 255)
    SELECTED_NODE_COLOR = (255, 255, 0)
    DRAGGING_NODE_COLOR = (255, 0, 0)

    BUTTON = (241, 241, 241)