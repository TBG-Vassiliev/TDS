import cv2
import numpy as np
from skimage import measure

# Charger l'image en niveaux de gris
image = cv2.imread('image.jpg', 0)

# Appliquer un filtre de détection de contours (par exemple, Canny)
edges = cv2.Canny(image, 70,90)
# cv2.imshow('Canny', edges)
# cv2.waitKey(0)

# Fermeture morphologique pour fermer les contours
kernel = np.ones((20, 20), np.uint8) # Grande taille de noyau, adapté manuellement pour notre image
closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Trouver les régions intérieures et extérieures
contours, hierarchy = cv2.findContours(closed_edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

# Classer les contours en fonction de leur aire pour détecter l'intérieur et l'extérieur
regions = []
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area > 2000:  # Filtrer les petits contours. Ajusté pour notre image
        regions.append((i, area))

regions.sort(key=lambda x: x[1], reverse=True)  # Trier les contours par aire

# Identifier l'intérieur et l'extérieur (les premiers sont les contours extérieurs)
outer_contour = contours[regions[0][0]]
inner_contours = [contours[regions[i][0]] for i in range(1, len(regions))]

# Dessiner les contours pour afficher l'intérieur et l'extérieur
output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(output, [outer_contour], -1, (0, 255, 0), 2)  # Contour extérieur en vert
cv2.drawContours(output, inner_contours, -1, (0, 0, 255), 2)  # Contours intérieurs en rouge

# Afficher l'image
cv2.imshow('Contours', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
