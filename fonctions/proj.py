import cv2
import numpy as np

# Charger l'image en niveau de gris
# Assurez-vous que le chemin de votre fichier est correct et accessible
image = cv2.imread('../TDS/images/image.jpg', cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Erreur lors du chargement de l'image")
else:
    # Affiche l'image dans une fenêtre nommée "Image"
    cv2.imshow("Image", image)

    # Attendez que l'utilisateur appuie sur une touche
    cv2.waitKey(0)

    # Ferme la fenêtre d'image
    cv2.destroyAllWindows()

# Définir les seuils pour les intervalles de foncé, moyen et clair
# Vous devrez peut-être ajuster ces seuils en fonction de votre image spécifique
seuil_fonce = 85
seuil_moyen = 170

# Créer une nouvelle image avec les mêmes dimensions que l'original
nouvelle_image = np.zeros_like(image)

# Zones foncées: tout pixel avec une intensité < seuil_fonce
nouvelle_image[image < seuil_fonce] = 0  # Noir

# Zones moyennes: tout pixel avec une intensité >= seuil_fonce ET < seuil_moyen
nouvelle_image[(image >= seuil_fonce) & (image < seuil_moyen)] = 127  # Gris

# Zones claires: tout pixel avec une intensité >= seuil_moyen
nouvelle_image[image >= seuil_moyen] = 255  # Blanc

# Sauvegarder la nouvelle image
# cv2.imwrite('chemin_vers_la_nouvelle_image.jpg', nouvelle_image)

# Afficher l'image dans une fenêtre
cv2.imshow('Image', nouvelle_image)
cv2.waitKey(0)  # attend que l'utilisateur appuie sur une touche
cv2.destroyAllWindows()


def appliquer_palette(image, couleurs):
    # Crée une image en couleur vide avec les mêmes dimensions
    image_couleur = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    # Applique les couleurs basées sur les seuils
    seuils = [85, 170]  # Ces seuils peuvent nécessiter des ajustements
    for i in range(3):
        # Pour chaque seuil, applique la couleur correspondante
        start_range = seuils[i-1] if i > 0 else 0
        end_range = seuils[i] if i < len(seuils) else 255
        mask = cv2.inRange(image, start_range, end_range)
        image_couleur[mask > 0] = couleurs[i]

    return image_couleur

# Charger l'image en niveau de gris
image = cv2.imread('H:\\Downloads\\shooting-nocturne-argentique.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Erreur lors du chargement de l'image")
    exit()

# Définit les palettes de couleurs pour chaque image
palettes = [
    [(255, 0, 0), (0, 255, 0), (0, 0, 255)],  # Rouge, vert, bleu
    [(0, 255, 255), (255, 0, 255), (255, 255, 0)],  # Cyan, magenta, jaune
    [(255, 125, 0), (125, 0, 255), (0, 255, 125)],  # Orange, violet, vert printemps
    [(255, 255, 255), (128, 128, 128), (0, 0, 0)],  # Blanc, gris, noir
    [(0, 100, 0), (139, 0, 0), (0, 0, 139)],  # Vert foncé, rouge foncé, bleu foncé
    [(255, 192, 203), (218, 112, 214), (173, 216, 230)]  # Rose, orchidée, bleu clair
]

# Crée le tableau d'images en couleurs
images_warhol = []
for palette in palettes:
    images_warhol.append(appliquer_palette(image, palette))

# Vérifiez que vous avez bien six images
if len(images_warhol) != 6:
    print("Erreur : il faut exactement six images pour le montage")
    exit()

# Combinez les images en une seule. Vous pouvez les arranger dans une configuration spécifique ici 2x3
hauteur, largeur = images_warhol[0].shape[:2]
montage = np.zeros((hauteur * 2, largeur * 3, 3), dtype=np.uint8)

positions = [(i, j) for i in range(2) for j in range(3)]
for (i, j), img in zip(positions, images_warhol):
    montage[i * hauteur:(i + 1) * hauteur, j * largeur:(j + 1) * largeur, :] = img

# Sauvegarder le montage
#cv2.imwrite('chemin_vers_le_montage.jpg', montage)

# Si le montage est trop grand pour être affiché, vous pouvez le redimensionner
facteur_echelle = 0.5  # réduire de 50%, vous pouvez modifier ce facteur selon vos besoins
hauteur_redimensionnee = int(montage.shape[0] * facteur_echelle)
largeur_redimensionnee = int(montage.shape[1] * facteur_echelle)

montage_redimensionne = cv2.resize(montage, (largeur_redimensionnee, hauteur_redimensionnee), interpolation=cv2.INTER_AREA)

# Afficher le montage redimensionné dans une fenêtre
cv2.imshow('Montage Warhol', montage_redimensionne)
cv2.waitKey(0)
cv2.destroyAllWindows()