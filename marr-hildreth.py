import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from scipy.ndimage import gaussian_laplace

# Charger l'image
image = imageio.imread('image.jpg', pilmode='L')

# Différentes valeurs de sigma, qui permettent de changer la force du flou (noyau gaussien)
sigmas = [1, 2, 3]

# Créer une figure avec une grille de sous-tracés pour afficher les différentes images filtrées
fig, axs = plt.subplots(1, len(sigmas) + 1, figsize=(15, 5))

# Afficher l'image originale
axs[0].imshow(image, cmap='gray')
axs[0].set_title('Image originale')

# Appliquer le filtre de Marr-Hildreth pour différentes valeurs de sigma et afficher les images filtrées
for i, sigma in enumerate(sigmas):
    filtered = gaussian_laplace(image, sigma=sigma) # Application du filtre
    # Ce filtre consistant à appliquer un filtre gaussien puis prendre le laplacien du résultat, 
    # nous utilisons ici la fonction "gaussian_laplace" que propose la bibliothèque scipy.
    axs[i + 1].imshow(filtered, cmap='gray')
    axs[i + 1].set_title(f'Sigma = {sigma}')

# Afficher les images
plt.tight_layout()
plt.show()