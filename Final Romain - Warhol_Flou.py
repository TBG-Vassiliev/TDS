import cv2
import numpy as np
import os


def capture_image_webcam():
    # Capture d'image depuis la webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Impossible d'ouvrir la webcam")
        exit()

    print("Appuyez sur 'Enter' pour capturer une image.")

    while True:
        ret, frame = cap.read()  # Lit une image depuis la webcam
        if not ret:
            print("Erreur lors de la capture de l'image, essayez à nouveau.")
            continue

        # Afficher l'image en direct
        cv2.imshow('Appuyez sur "Enter" pour capturer', frame)

        # Si 'Enter' est appuyé, l'image est capturée et la boucle est rompue
        if cv2.waitKey(1) & 0xFF == 13:  # 13 est le code ASCII pour 'Enter'
            break

    # Quand l'image est prise, libérer la caméra et fermer toutes les fenêtres actives
    cap.release()
    cv2.destroyAllWindows()

    return frame

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

"""
Dans le contexte du flou gaussien, augmenter la taille du noyau intensifie l'effet de flou. Voici une explication détaillée :

Définition du noyau : Un "noyau" est une matrice utilisée pour l'application d'opérations telles que le flou sur une image. Il détermine comment chaque pixel est ajusté en fonction des pixels environnants.

Fonctionnement du flou gaussien : Ce type de flou utilise une fonction gaussienne pour créer un noyau. Chaque pixel de l'image est modifié en fonction de la moyenne pondérée des pixels environnants, les poids étant déterminés par le noyau gaussien. En gros, chaque pixel est "mélangé" avec ses voisins, avec une influence décroissante à mesure qu'on s'éloigne du pixel central.

Impact de la taille du noyau : La taille du noyau détermine le nombre de pixels environnants pris en compte lors du "mélange". Un noyau plus grand augmente cette zone, faisant que chaque pixel est influencé par un ensemble plus large de voisins, ce qui se traduit par un flou plus intense.

En résumé, une taille de noyau plus grande dans un flou gaussien signifie que chaque pixel est mélangé avec un plus grand nombre de pixels voisins, ce qui résulte en un effet de flou plus prononcé. Cependant, il est important de trouver un équilibre, car un noyau excessivement grand peut entraîner la perte de détails importants dans l'image.
"""

# La taille doit obligatoirement etre impaire. C'est exigé par OpenCV
def appliquer_flou(image, taille_kernel=(101, 101)):
    """
    Applique un flou gaussien à l'image fournie en utilisant la taille du noyau spécifiée.

    :param image: Image à flouter.
    :param taille_kernel: Tuple spécifiant la taille du noyau du flou gaussien.
    :return: Image floutée.
    """
    return cv2.GaussianBlur(image, taille_kernel, 0)

def main():
    # Capture d'image
    image_couleur = capture_image_webcam()
    if image_couleur is None:
        print("Erreur lors de la capture de l'image.")
        exit()
        
    # Convertir l'image en niveau de gris
    image_gris = cv2.cvtColor(image_couleur, cv2.COLOR_BGR2GRAY)

    # Convertir l'image en niveau de gris de retour en BGR pour que les deux images aient le même nombre de canaux
    image_gris_en_couleur = cv2.cvtColor(image_gris, cv2.COLOR_GRAY2BGR)

    # Combiner les images horizontalement
    images_combinees = np.hstack((image_couleur, image_gris_en_couleur))

    # Afficher les images combinées
    cv2.imshow('Image en Couleur et Image en Gris', images_combinees)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    
    # Appliquer un flou gaussien
    montage_flou = appliquer_flou(montage)

    # Afficher le montage flou dans une fenêtre
    cv2.imshow('Montage Warhol Flou A Payer', montage_flou)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Afficher le montage dans une fenêtre
    cv2.imshow('Montage Warhol', montage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Enregistrer l'image floutée sur le bureau
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    cv2.imwrite(os.path.join(desktop, 'montage_warhol_flou.png'), montage_flou)
    
    
if __name__ == "__main__":
    main()