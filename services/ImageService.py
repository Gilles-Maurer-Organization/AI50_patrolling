import os
import shutil
from pathlib import Path
from services.IImageService import IImageService

class ImageService(IImageService):
    def __init__(self) -> None:
        # folder to store background images
        self.backgrounds_folder = Path(__file__).resolve().parent.parent / "backgrounds"
        if not self.backgrounds_folder.exists():
            os.makedirs(self.backgrounds_folder)

    def is_an_image(self, image_name: str) -> bool:
        return image_name.lower().endswith(('.png', '.jpg', '.jpeg'))

    def check_if_image_exists(self, image_path: str) -> None:
        image_name = os.path.basename(image_path)
        project_image_path = self.backgrounds_folder / image_name
        if not project_image_path.exists():
            print(f"Image '{image_name}' not found in the backgrounds folder, copying...")
            shutil.copy(image_path, project_image_path)
        else:
            print(f"Image '{image_name}' found in the backgrounds folder.")
