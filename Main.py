# Import de nos fonctions

from fonctions.essai import *
# from fonctions.Convolution2 import *
# from fonctions.Warhol_Flou import *
# from fonctions.gradient import *
# from fonctions.interface import *
from fonctions.internextern import *
from fonctions.marr_hildreth import *
# from fonctions.proj import *
# from fonctions.proj2 import *

# Import des autres modules

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import shutil
import os

image = choisir_image()


# ================= Définition des fonctions que les boutons vont appeler ======================================


def afficher_image_original():
        cv2.imshow("Image originale", image)

def afficher_contours():
    contours, _, _ = detecter_contours(image)
    cv2.imshow("Contours", contours)

def afficher_gradients():
    _, dI_dx, dI_dy = detecter_contours(image)
    cv2.imshow("Gradient - dI/dx", dI_dx)
    cv2.imshow("Gradient - dI/dy", dI_dy)

def afficher_bd():
    image_bd = transformer_en_image_bd(image)
    cv2.imshow("Image de bande dessinée", image_bd)


# Convertir l'image en niveau de gris
image_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Convertir l'image en niveau de gris de retour en BGR pour que les deux images aient le même nombre de canaux
image_gris_en_couleur = cv2.cvtColor(image_gris, cv2.COLOR_GRAY2BGR)

# Combiner les images horizontalement
images_combinees = np.hstack((image, image_gris_en_couleur))

def afficher_image_combinees():
        # Afficher les images combinées
        cv2.imshow('Image en Couleur et Image en Gris', images_combinees)

   
    # Définit les palettes de couleurs pour chaque image
palettes = [
    [(255, 0, 0), (0, 255, 0), (0, 0, 255)],  # Rouge, vert, bleu
    [(0, 0, 0), (127, 127, 127), (255, 255, 255)],  # Noir, gris, blanc
    [(255, 255, 0), (0, 255, 255), (255, 0, 255)],  # Jaune, cyan, magenta
    [(0, 0, 128), (0, 128, 0), (128, 0, 0)],  # Bleu marine, vert, bordeaux
    [(128, 0, 128), (0, 128, 128), (128, 128, 0)],  # Pourpre, teal, olive
    [(255, 165, 0), (255, 20, 147), (30, 144, 255)],  # Orange, rose vif, bleu Dodger
]

    # Crée le tableau d'images en couleurs
images_warhol = []
for palette in palettes:
    images_warhol.append(appliquer_palette(image_gris, palette))

# Combinez les images en une seule
hauteur, largeur = images_warhol[0].shape[:2]
montage = np.zeros((hauteur * 2, largeur * 3, 3), dtype=np.uint8)

positions = [(i, j) for i in range(2) for j in range(3)]
for (i, j), img in zip(positions, images_warhol):
    montage[i * hauteur:(i + 1) * hauteur, j * largeur:(j + 1) * largeur, :] = img

# Redimensionnez le montage final si nécessaire
hauteur_finale = 800  # ou toute autre hauteur souhaitée
largeur_finale = int(hauteur_finale * (largeur * 3) / (hauteur * 2))  # pour conserver les proportions

montage = cv2.resize(montage, (largeur_finale, hauteur_finale))

# Enregistrer l'image sur le bureau
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
cv2.imwrite(os.path.join(desktop, 'montage_warhol.png'), montage)

# Appliquer un flou gaussien au montage
montage_flou = appliquer_flou(montage)

def afficher_montage_flou():
    # Afficher le montage flou dans une fenêtre
    cv2.imshow('Montage Warhol Flou A Payer avec Methode Gaussienne', montage_flou)

# Appliquer un flou SVD au montage
image_floue = appliquer_svd_flou(montage)  # vous pouvez ajuster k en fonction de vos besoins
    
def afficher_image_flou():
    cv2.imshow('Montage Warhol Flou A Payer avec Methode SVD', image_floue)

def afficher_montage_warhol():
    # Afficher le montage dans une fenêtre
    cv2.imshow('Montage Warhol', montage)

# Enregistrer l'image floutée sur le bureau
cv2.imwrite(os.path.join(desktop, 'montage_warhol_flou.png'), image_floue)

def afficher_filtre_MH():
    marrhildreth(image)

def afficher_zones_IE():
    interextern(image)



# ================================ Fin des fonctions des boutons ===============================================


def button_clicked(function_name):
    function = globals().get(function_name)
    if function:
        function()
    else:
        print(f"La fonction {function_name} n'a pas été définie")

root = tk.Tk()
root.title("Menu")

# Noms des boutons
button_names = [
    "Image originale",
    "Contours",
    "Gradients",
    "Image de bande dessinée",
    "Image combinée",
    "Montage flou",
    "Image flou",
    "Montage Warhol",
    "Marr-Hildreth",
    "Zones interne/externe"
]

button_commands = [
    "afficher_image_original",
    "afficher_contours",
    "afficher_gradients",
    "afficher_bd",
    "afficher_image_combinees",
    "afficher_montage_flou",
    "afficher_image_flou",
    "afficher_montage_warhol",
    "afficher_filtre_MH",
    "afficher_zones_IE"
]

# Utilisation du thème "adapta"
style = ThemedStyle(root)
style.set_theme("adapta")

# Création des boutons avec les noms spécifiés
for i, (name, command) in enumerate(zip(button_names, button_commands)):
    row = i // 5
    col = i % 5
    button = ttk.Button(root, text=name, command=lambda cmd=command: button_clicked(cmd), width=20)
    button.grid(row=row, column=col, padx=5, pady=5)

root.mainloop()



# Suppression du répertoire __pycache__ à la fin de l'exécution
directory = 'fonctions/__pycache__'

try:
    shutil.rmtree(directory)
    print(f"Le repertoire {directory} a ete supprime.")
except FileNotFoundError:
    print(f"Le repertoire {directory} n'existe pas.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
