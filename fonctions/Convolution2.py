import numpy as np
import matplotlib.pyplot as plt
from scipy import signal #pour la convolution
import imageio.v2 as imageio #pour lire à partir d'un fichier

#lecture de l'image originale
A = np.asarray(imageio.imread('../TDS/images/image.jpg')) 

#si l'image est en couleur, on la passe en noir & blanc
if len(A.shape) == 3: 
    A = np.mean(A, axis=2) #la valeur du pixel noir&blanc vaut la moyenne du pixel sur les 3 couleurs
    
#Masques utilisés pour déterminer le gradient de l'image dans les  directions
H1 = np.array([[-1,0,1],[-5,0,5],[-1,0,1]]) # gradient horizontal 
H2 = np.array([[-1,-5,-1],[0,0,0],[1,5,1]]) # gradient vertical
M = np.array([[1/5,1/5,1/5],[1/5,1/5,1/5],[1/5,1/5,1/5]]) #éclaircit l'image devrait flouter en théorie
M2 = np.array([[-1.125,0,1.125],[-0.25,0,0.25],[-1.125,0,1.125]])

#Application des convolutions selon plusieurs matrices
B = signal.convolve2d(A, M,mode='same') # applique la convolution de A avec le noyau M, l'image résultante est de la même taille que A
B[B>255]=255 #ajustement des valeurs de B pour que B appartienne à [0;255] comme c'est un pixel représentant une couleur
B[B<0]=0
#B=255-B #contours noirs sur fond blanc (=image noir et blanc en négative)

C = signal.convolve2d(A, M2,mode='same') # applique la convolution de A avec le noyau M, l'image résultante est de la même taille que A
C[C>255]=255 #ajustement des valeurs de B pour que B appartienne à [0;255] comme c'est un pixel représentant une couleur
C[C<0]=0
#B=255-B #contours noirs sur fond blanc (=image noir et blanc en négative)

G1 = signal.convolve2d(A, H1,mode='same') # applique la convolution de A avec le noyau M, l'image résultante est de la même taille que A
G1[G1>255]=255 #ajustement des valeurs de B pour que B appartienne à [0;255] comme c'est un pixel représentant une couleur
G1[G1<0]=0
#G1=255-G1 #contours noirs sur fond blanc (=image noir et blanc en négative)

G2 = signal.convolve2d(A, H2,mode='same') # applique la convolution de A avec le noyau M, l'image résultante est de la même taille que A
G2[G2>255]=255 #ajustement des valeurs de B pour que B appartienne à [0;255] comme c'est un pixel représentant une couleur
G2[G2<0]=0
#G2=255-G2 #contours noirs sur fond blanc (=image noir et blanc en négative)

#affichage des images
print("Chargement des images...")
plt.figure("Image originale")
plt.imshow(A,cmap="gray")
plt.figure("Matrice de convolution tout élément du même poids (1/5)")
plt.imshow(B,cmap="gray")
plt.figure("C")
plt.imshow(C,cmap="gray")
plt.figure("Gradient 1 (horizontal)")
plt.imshow(G1,cmap="gray")
plt.figure("Gradient 2 (vertical)")
plt.imshow(G2,cmap="gray")
plt.show()