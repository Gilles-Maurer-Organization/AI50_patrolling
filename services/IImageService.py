from abc import ABC, abstractmethod

class IImageService(ABC):
    @abstractmethod
    def is_an_image(self, image_name: str) -> bool:
        pass

    @abstractmethod
    def check_if_image_exists(self, image_path: str) -> None:
        pass
    
    @abstractmethod
    def ensure_image_exists_and_copy(self, image_path: str) -> None:
        pass