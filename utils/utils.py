import os
import sys

def resource_path(relative_path):
    """Return the absolute path to a resource, accounting for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
