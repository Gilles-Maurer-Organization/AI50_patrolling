from enum import Enum

class Colors(Enum):
    """
    Enumeration defining the colors used in the program (node colors,
    node selection color, edge colors, etc.)
    """
    
    # General colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # Node-related colors
    NODE_COLOR_MIN = (204, 179, 149)  # Gradient start
    NODE_COLOR_MAX = (217, 4, 41)    # Gradient end
    SELECTED_NODE_COLOR = (237, 205, 93)
    DRAGGING_NODE_COLOR = (188, 132, 67)
    EDGE_COLOR = (105, 105, 105)     # Edge color

    # Grayscale shades
    ICE_GRAY = (248, 248, 248)
    FOG_GRAY = (241, 241, 241)
    PEARL_GRAY = (226, 226, 226)
    SILVER_GRAY = (200, 200, 200)
    ASH_GRAY = (166, 166, 166)
    PLATINUM_GRAY = (220, 220, 220)
    
    GREEN = (155, 219, 162)          # Default green
    DARK_GREEN = (105, 201, 115)     # Highlighted green
    RED = (250, 184, 184)            # Default red
    DARK_RED = (247, 141, 141)       # Highlighted red
    ORANGE = (255, 182, 92)          # Default orange
    DARK_ORANGE = (255, 162, 49)     # Highlighted orange
    DISABLED = (245, 235, 235)       # Disabled button color
    
    # Popup-related colors
    POPUP_ERROR_COLOR = (245, 34, 45, 215)   # Red with transparency
    POPUP_INFO_COLOR = (250, 140, 22, 215)   # Orange with transparency
    POPUP_COLOR = (82, 196, 26, 215)         # Green with transparency