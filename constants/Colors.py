from enum import Enum

class Colors(Enum):
    '''
    Enumération permettant de définir les couleurs utilisés dans le programme (couleur des noeuds, couleur de sélection d'un noeud, couleur des liens, etc)
    '''
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    NODE_COLOR = (204, 179, 149)
    SELECTED_NODE_COLOR = (237, 205, 93)
    DRAGGING_NODE_COLOR = (188, 132, 67)
    EDGE_COLOR = (105, 105, 105)

    LIGHT_GRAY = (248, 248, 248)

    # Relatif aux boutons
    BUTTON = (241, 241, 241)
    BUTTON_HOVER = (226, 226, 226)
    BUTTON_GREEN = (155, 219, 162)
    BUTTON_GREEN_HOVER = (105, 201, 115)
    BUTTON_RED = (250, 184, 184)
    BUTTON_RED_HOVER = (247, 141, 141)
    GRAY_TEXT = (200, 200, 200)

    BUTTON_DISABLED = (245, 235, 235)

    # Relatif aux textbox
    TEXT_BOX_TEXT = (166, 166, 166)
    TEXT_BOX_CLICKED = (220, 220, 220)
