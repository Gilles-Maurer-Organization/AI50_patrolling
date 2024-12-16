import os

import pygame

class AgentView:
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
            position: A tuple (x, y) indicating where to draw the image.
        """
        if self._image:
            offset_x = self._image_width // 2
            offset_y = self._image_height // 2
            centered_position = (position[0] - offset_x, position[1] - offset_y)
            
            self._screen.blit(self._image, centered_position)
        else:
            raise ValueError("The image has not been loaded properly.")