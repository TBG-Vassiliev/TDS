# Import de nos fonctions

from fonctions.essai import *
# from fonctions.Convolution2 import *
# from fonctions.Warhol_Flou import *
# from fonctions.gradient import *
# from fonctions.interface import *
# from fonctions.internextern import *
# from fonctions.marr_hildreth import *
# from fonctions.proj import *
# from fonctions.proj2 import *

# Import des autres modules

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import shutil
import os


def button_clicked(button_name):
    print(f"Bouton {button_name} clique")

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

# Utilisation du thème "adapta"
style = ThemedStyle(root)
style.set_theme("adapta")

# Création des boutons avec les noms spécifiés
for i, name in enumerate(button_names):
    row = i // 5
    col = i % 5
    button = ttk.Button(root, text=name, command=lambda name=name: button_clicked(name), width=20)
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
