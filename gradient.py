import cv2
import numpy as np


#lit une image en noir et blanc
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

#filtre de Sobel
dI_dx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
dI_dy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

#calcul module du gradient
moduleGradient = np.sqrt(dI_dx**2 + dI_dy**2)

#seuil défini en fonction de notre image
seuil_module = 50

#contour obtenu avec binarisation de l'image : si module du gradient > seuil => contour
contours_module = (moduleGradient > seuil_module).astype(np.uint8) * 255

#image du gradient x
cv2.imshow('Gradient - dI/dx', dI_dx)

#image du gradient y
cv2.imshow('Gradient - dI/dy', dI_dy)

#image module
cv2.imshow('Contours - Sobel/seuillage', contours_module)

cv2.waitKey(0)
cv2.destroyAllWindows()


#Les zones de l'image où le gradient est important apparaîtront plus lumineuses, tandis que les zones avec un faible gradient seront plus sombres =>  indicateur présence contours significatifs
