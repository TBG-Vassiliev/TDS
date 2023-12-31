import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mon Application de Traitement d’Images')

        # Layout vertical pour placer les widgets
        vbox = QVBoxLayout()

        # Bouton pour capturer l'image
        btnCapture = QPushButton('Capturer Image', self)
        btnCapture.clicked.connect(self.captureImage)
        vbox.addWidget(btnCapture)

        # Label pour afficher l'image
        self.imageLabel = QLabel(self)
        vbox.addWidget(self.imageLabel)

        # Bouton pour appliquer le flou
        btnBlur = QPushButton('Appliquer Flou', self)
        btnBlur.clicked.connect(self.applyBlur)
        vbox.addWidget(btnBlur)

        # Autres boutons et widgets peuvent être ajoutés ici...

        self.setLayout(vbox)


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

# k est le nombre de valeurs singulières
def appliquer_svd_flou(image, k=10):
    """
    Applique un flou à l'image en utilisant la décomposition en valeurs singulières (SVD).

    :param image: Image à flouter.
    :param k: Nombre de valeurs singulières à conserver.
    :return: Image floutée.
    """
    # Convertir l'image en double précision, format nécessaire pour la SVD en numpy
    img = image.astype(np.float64)

    # La SVD s'applique sur des matrices 2D, nous devons donc appliquer SVD sur chaque canal de couleur séparément
    canaux = cv2.split(img)  # Séparer les canaux de couleur
    canaux_reconstruits = []
    for canal in canaux:
        # Appliquer la SVD
        U, S_diag, VT = np.linalg.svd(canal, full_matrices=False)

        # Assurez-vous que k ne dépasse pas le nombre de valeurs singulières
        k = min(k, len(S_diag))

        # Écraser S (les valeurs singulières) avec les k premières valeurs puis tout le reste à zéro
        S_diag_k = np.zeros_like(S_diag)
        S_diag_k[:k] = S_diag[:k]

        # Convertir S en une matrice diagonale
        S = np.diag(S_diag_k)

        # Reconstruire l'image
        canal_reconstruit = np.dot(U, np.dot(S, VT))
        canaux_reconstruits.append(canal_reconstruit)

    # Fusionner les canaux de couleur
    img_reconstruite = cv2.merge(canaux_reconstruits)

    # S'assurer que les valeurs sont dans le bon intervalle pour uint8 [0, 255]
    img_reconstruite[img_reconstruite > 255] = 255
    img_reconstruite[img_reconstruite < 0] = 0

    # Convertir en uint8
    img_reconstruite = img_reconstruite.astype(np.uint8)

    return img_reconstruite


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
    cv2.imshow('Montage Warhol Flou A Payer avec Methode Gaussienne ', montage_flou)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    image_floue = appliquer_svd_flou(montage)  # vous pouvez ajuster k en fonction de vos besoins

    # Afficher l'image floutée
    cv2.imshow('Montage Warhol Flou A Payer avec Methode SVD', image_floue)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Afficher le montage dans une fenêtre
    cv2.imshow('Montage Warhol A Enregistrer dans votre Dossier contenant le code', montage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Enregistrer l'image floutée sur le bureau
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'H:\Desktop\Projet traitement signal') 
    cv2.imwrite(os.path.join(desktop, 'montage_warhol.png'), montage)
    
    
#if __name__ == "__main__":
 #   main()
 
 ###############################################################################################
 #Partie interface
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QCursor  # QCursor est importé depuis QtGui
from PyQt5.QtCore import Qt

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Palette de couleurs claires pour une apparence simple et propre
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)  # Fond blanc pour la fenêtre
        palette.setColor(QPalette.WindowText, Qt.black)  # Texte noir
        self.setPalette(palette)

        self.setWindowTitle('VisionArtiste')
        self.setWindowIcon(QIcon('path/to/your/icon.png'))  # Remplacez par le chemin de votre icône

        vbox = QVBoxLayout()

        # Ajouter un QLabel pour l'explication de l'application
        explanationLabel = QLabel("Cette application vous permet de transformer vos images en œuvres. Sélectionnez une image et appliquez des effets artistiques uniques!", self)
        explanationLabel.setWordWrap(True)  # Permettre le retour à la ligne automatique
        explanationLabel.setFont(QFont('SansSerif', 10))
        vbox.addWidget(explanationLabel)

        btnStart = QPushButton('Créer un Oeuvre d\'art style Andy Warhol', self)

        btnStart.clicked.connect(self.startImageProcessing)
        btnStart.setFont(QFont('SansSerif', 10))
        btnStart.setCursor(QCursor(Qt.PointingHandCursor))  # Change le curseur en main pointante lorsqu'il survole le bouton
        btnStart.setStyleSheet("""
            background-color: #4CAF50;  /* Vert */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 4px;
            cursor: pointer;
        """)
        vbox.addWidget(btnStart)

        # Ajoutez ici d'autres widgets si nécessaire...

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 200)  # Vous pouvez ajuster la taille si nécessaire pour s'adapter au texte d'explication

    def startImageProcessing(self):
        main()  # La fonction principale pour le traitement d'image

# ... Votre code pour capture_image_webcam, appliquer_palette, appliquer_flou, appliquer_svd_flou, et main ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SimpleApp()
    ex.show()
    sys.exit(app.exec_())

