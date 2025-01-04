import os
import shutil
from pathlib import Path

from models.Info import Info
from services.IImageService import IImageService


class ImageService(IImageService):
    def __init__(self) -> None:
        # folder to store background images
        self.backgrounds_folder = (
            Path(__file__).resolve().parent.parent / "backgrounds"
        )
        if not self.backgrounds_folder.exists():
            os.makedirs(self.backgrounds_folder)

    def is_an_image(self, image_name: str) -> bool:
        """
        Checks if the given image name is in a valid image format (PNG,
        JPG, JPEG).
        
        Args:
            image_name (str): Name of the image file.
        
        Returns:
            bool: True if the file is an image, False otherwise.
        """
        return image_name.lower().endswith(('.png', '.jpg', '.jpeg'))

    def check_if_image_exists(self, image_path: str) -> bool:
        """
        Checks if the image already exists in the backgrounds folder.

        Args:
            image_path (str): Path to the image to check.
        
        Returns:
            bool: True if the image exists, False otherwise.
        """
        image_name = os.path.basename(image_path)
        project_image_path = self.backgrounds_folder / image_name
        return project_image_path.exists()

    def ensure_image_exists_and_copy(self, image_path: str) -> None:
        """
        Ensures the image exists in the backgrounds folder. If not,
        copy it there.
        
        Args:
            image_path (str): Path to the image to ensure and copy.
        """
        image_name = os.path.basename(image_path)
        project_image_path = self.backgrounds_folder / image_name
        if not self.check_if_image_exists(image_path):
            if not os.path.exists(image_path):
                return
            shutil.copy(image_path, project_image_path)
