from abc import ABC, abstractmethod

class IImageService(ABC):
    """
    Interface for image services, providing methods for checking, 
    validating, and copying image files in a project.
    """
    @abstractmethod
    def is_an_image(self, image_name: str) -> bool:
        """
        Checks if the provided file name corresponds to an image.
        """
        pass

    @abstractmethod
    def check_if_image_exists(self, image_path: str) -> None:
        """
        Checks if the image already exists in the target folder.
        """
        pass
    
    @abstractmethod
    def ensure_image_exists_and_copy(self, image_path: str) -> None:
        """
        Ensures that the image exists in the target folder. If not, 
        it copies the image to the folder.
        """
        pass