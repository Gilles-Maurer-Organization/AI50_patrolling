from PIL import Image
import tkinter
from tkinter import filedialog

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

folder_path = filedialog.askopenfilename() # Ouvre l'explorateur de fichier pour sélectionner l'image

im = Image.open(folder_path)
im.show() # Affiche l'image