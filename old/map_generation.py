import pygame
import sys
import os
from pathlib import Path
from PIL import Image


# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)

tile_size = 40  # Taille de chaque carreau en pixels
player_pos = None

current_max = 0 
total_max = 0

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


def create_image_map(data):

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
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)

            for i in range(tile_size):
                for j in range(tile_size):
                    # Remplir chaque case (carreau)
                    image.putpixel((x * tile_size + i, y * tile_size + j), color)

    # # Sauvegarder l'image
    # image.save('quadrillage.png')

    # Afficher l'image
    image.show()


def init_game_window(data): 

    # Initialiser Pygame
    pygame.init()

    # Paramètres de la carte
    width = len(data[0])  # Largeur en carreaux
    height = len(data)  # Hauteur en carreaux
    screen_width = width * tile_size
    screen_height = height * tile_size


    # Créer la fenêtre
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Carte Multi-Agent")

    return screen


def find_color_cell(cell, time_data):

    match cell: 

        case 0: return BLACK
        case 1: return PINK if time_data == current_max else WHITE 
        case 2: return GREEN


def draw_map(data, time_data, screen): 

    font = pygame.font.SysFont(None, 24)  # Définir une police pour afficher les textes

    for y, row in enumerate(data):
            for x, cell in enumerate(row):
                # Définir la couleur en fonction de la valeur de la matrice
                color = find_color_cell(cell, time_data[y][x])
                pygame.draw.rect(screen, color, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))

                # Si la cellule est blanche (passage), écrire la valeur correspondante de time_data
                if cell == 1:
                    # Créer le texte avec la valeur de time_data[y][x]
                    text_surface = font.render(str(time_data[y][x]), True, (0, 0, 0))  # Noir pour le texte
                    # Centrer le texte dans la cellule
                    text_rect = text_surface.get_rect(center=(x * tile_size + tile_size // 2, y * tile_size + tile_size // 2))
                    # Dessiner le texte sur l'écran
                    screen.blit(text_surface, text_rect)


def move_player(data, time_data, direction):

    global player_pos
    x, y = player_pos
    
    # Vérifier la direction et la nouvelle position
    if direction == "UP" and y > 0 and data[y-1][x] != 0:
        data[y][x] = 1  # Remettre l'ancienne position à 1 (chemin)
        time_data[y-1][x] = 0
        player_pos = [x, y-1]
    elif direction == "DOWN" and y < len(data)-1 and data[y+1][x] != 0:
        data[y][x] = 1
        time_data[y+1][x] = 0
        player_pos = [x, y+1]
    elif direction == "LEFT" and x > 0 and data[y][x-1] != 0:
        data[y][x] = 1
        time_data[y][x-1] = 0
        player_pos = [x-1, y]
    elif direction == "RIGHT" and x < len(data[0])-1 and data[y][x+1] != 0:
        data[y][x] = 1
        time_data[y][x+1] = 0
        player_pos = [x+1, y]
    
    # Mettre à jour la position du joueur (2)
    data[player_pos[1]][player_pos[0]] = 2


def find_initial_position(data):
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == 1:  # Trouver la première case blanche
                data[y][x] = 2  # Placer le joueur à cet endroit
                return (x, y)  # Retourner la position du joueur
    return None  # Si aucune case blanche n'est trouvée


def create_time_data(data):
    # Initialiser le tableau time_data avec la même taille que data
    time_data = []
    
    # Parcourir chaque ligne de data
    for row in data:
        # Créer une nouvelle ligne pour time_data
        new_row = []
        for cell in row:
            if cell == 0:
                new_row.append(-1)  # Murs (0) -> -1 dans time_data
            elif cell == 1:
                new_row.append(0)   # Passages (1) -> 0 dans time_data
        # Ajouter la nouvelle ligne à time_data
        time_data.append(new_row)
    
    return time_data

def increment_time_data(time_data):

    max = 0

    for y in range(len(time_data)):
        for x in range(len(time_data[y])):
            if time_data[y][x] != -1:
                time_data[y][x] += 1

                if (time_data[y][x] > max) : max = time_data[y][x] 

    global current_max 
    current_max = max

    global total_max
    if current_max > total_max : total_max = current_max 

    return time_data

def main():

    data = open_file('map1.csv')
    data = [[int(item) for item in row] for row in data]

    last_update_time = pygame.time.get_ticks()  # Obtenir le temps écoulé en millisecondes depuis le lancement du programme



    # print(data)
    # create_image_map(data)


    time_data = create_time_data(data)

    screen = init_game_window(data)

    global player_pos
    player_pos = find_initial_position(data)
    if not player_pos:
        pygame.quit()
        sys.exit()

    data[player_pos[1]][player_pos[0]] = 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(data, time_data, "UP")
                elif event.key == pygame.K_DOWN:
                    move_player(data, time_data, "DOWN")
                elif event.key == pygame.K_LEFT:
                    move_player(data, time_data, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_player(data, time_data, "RIGHT")

        current_time = pygame.time.get_ticks()  # Obtenir le temps écoulé en millisecondes depuis le lancement du programme

        if (current_time - last_update_time >= 1000) :
            increment_time_data(time_data)
            last_update_time = current_time

        # Dessiner la carte
        screen.fill(BLACK)
        draw_map(data, time_data, screen)
      

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

    print(total_max)


    sys.exit()





if __name__ == "__main__":
    main()

