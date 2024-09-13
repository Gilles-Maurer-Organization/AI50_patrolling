
import os
from pathlib import Path
from PIL import Image



# os.path.join(get_dir_path(), file_name)

def open_file(file_name):
    file_path = os.path.join(get_dir_path(), file_name)

    # mettre les données dans un tableau
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line.strip().split(','))

    return data
    

def get_dir_path():
    # Obtenir le chemin du fichier en cours
    return Path(__file__).resolve().parent


def create_map(data):

    # Taille d'un carreau
    tile_size = 20

    # Taille de l'image basée sur la taille du quadrillage
    img_width = len(data[0]) * tile_size
    img_height = len(data) * tile_size

    # Créer une image RGB
    image = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))

    # Parcourir la table et remplir l'image
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            # Définir la couleur en fonction de la valeur du tableau (1 = blanc, 0 = noir)
            color = (255, 255, 255) if cell == '1' else (0, 0, 0)

            for i in range(tile_size):
                for j in range(tile_size):
                    # Remplir chaque case (carreau)
                    image.putpixel((x * tile_size + i, y * tile_size + j), color)

    # # Sauvegarder l'image
    # image.save('quadrillage.png')

    # Afficher l'image
    image.show()


def main():

    data = open_file('map2.csv')

    # print(data)
    create_map(data)




if __name__ == "__main__":
    main()

