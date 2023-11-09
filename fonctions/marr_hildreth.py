import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from scipy.ndimage import gaussian_laplace

# Charger l'image exemple
image = imageio.imread('../images/image2.png')

def marrhildreth(image):
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Différentes valeurs de sigma, qui permettent de changer la force du flou (noyau gaussien)
    sigmas = [1, 2, 3]

    # Afficher l'image originale dans une fenêtre séparée
    plt.figure("Image originale")
    plt.imshow(gray_image, cmap='gray')
    plt.title('Image originale en niveaux de gris')

    # Appliquer le filtre de Marr-Hildreth pour différentes valeurs de sigma et afficher les images filtrées dans des fenêtres séparées
    for sigma in sigmas:
        filtered = gaussian_laplace(gray_image, sigma=sigma)
        # Ce filtre consistant à appliquer un filtre gaussien puis prendre le laplacien du résultat, 
        # nous utilisons ici la fonction "gaussian_laplace" que propose la bibliothèque scipy.
        plt.figure(f'Image filtrée avec Sigma = {sigma}')
        plt.imshow(filtered, cmap='gray')
        plt.title(f'Image filtrée avec Sigma = {sigma}')

    # Afficher les images
    plt.show()
