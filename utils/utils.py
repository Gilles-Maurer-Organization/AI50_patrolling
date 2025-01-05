import os
import sys
from pathlib import Path

def resource_path(relative_path):
    """Return the absolute path to a static asset, accounting for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_data_path(subfolder: str = "") -> Path:
    """
    Returns the path to the data folder, considering whether the program
    is running in a PyInstaller environment or not.
    
    Args:
        subfolder (str): A specific subfolder inside the data directory.

    Returns:
        Path: The full path to the requested directory or file.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller environment
        base_path = Path(os.path.dirname(sys.executable))
        data_folder = base_path / 'data'
    else:
        # Development environment
        data_folder = Path(__file__).resolve().parent.parent
    
    if subfolder:
        return data_folder / subfolder
    return data_folder