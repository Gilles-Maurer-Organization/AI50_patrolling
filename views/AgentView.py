import os

import pygame

class AgentView:
    """
    This class draws an agent on the view of the graph.

    Attributes:
        _screen (pygame.Surface): The surface on which the agent is drawn.
        _image_path (str): The path of the agent's image.
        _self._image (pygame.Surface): The surface of agent's image on the
            graph.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._image_path = "assets/agent/agent.png"

        if os.path.exists(self._image_path):
            self._image = pygame.image.load(self._image_path)
            self._image = pygame.transform.scale(self._image, (44, 44))
            self._image_width, self._image_height = self._image.get_size()
        else:
            raise FileNotFoundError(f"The file at path '{self._image_path}' does not exist.")
        
    def draw(self, position: tuple[int, int]) -> None:
        """
        Draws the agent's image on the screen at the specified position.

        Args:
            position (tuple[int, int]): A tuple (x, y) indicating where to draw the image.
        """
        if self._image:
            offset_x = self._image_width // 2
            offset_y = self._image_height // 2
            centered_position = (position[0] - offset_x, position[1] - offset_y)
            
            self._screen.blit(self._image, centered_position)
        else:
            raise ValueError("The image has not been loaded properly.")