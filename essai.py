import cv2
import numpy as np
import os
import pyautogui
import tkinter as tk
from tkinter import ttk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QCursor  # QCursor est importé depuis QtGui
from PyQt5.QtCore import Qt


def capture_image_webcam():
    # Capture d'image depuis la webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Impossible d'ouvrir la webcam")
        return None

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

# Fonction pour redimensionner l'image
def redimensionner_si_trop_grande(image):
    ecran_largeur, ecran_hauteur = pyautogui.size()
    hauteur_cible = ecran_hauteur // 2  # La hauteur cible est la moitié de la hauteur de l'écran

    if image.shape[1] > ecran_largeur:
        ratio = ecran_largeur / image.shape[1]
        largeur_cible = ecran_largeur
        image_redimensionnee = cv2.resize(image, (largeur_cible, hauteur_cible))
        return image_redimensionnee
    else:
        return image

# Fonction pour choisir une image enregistré dans l'ordinateur
def choisir_image():
    print("Choisissez une option :")
    print("1. Capturer une image depuis la webcam")
    print("2. Sélectionner une image depuis le système de fichiers")

    option = input("Entrez le numéro de l'option choisie (1 ou 2) : ")

    if option == "1":
        image = capture_image_webcam()
    elif option == "2":
        chemin_image = input("Entrez le chemin complet de l'image : ")
        image = cv2.imread(chemin_image)

        if image is None:
            print("Erreur lors de la lecture de l'image depuis le chemin spécifié.")
            return None
    else:
        print("Option non valide.")
        return None

    # Redimensionner l'image si elle est trop grande
    image = redimensionner_si_trop_grande(image)
    return image

# Fonction pour détecter les contours
def detecter_contours(image):
    # Convertir l'image en niveaux de gris
    image_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Filtre de Sobel
    dI_dx = cv2.Sobel(image_gris, cv2.CV_64F, 1, 0, ksize=3)
    dI_dy = cv2.Sobel(image_gris, cv2.CV_64F, 0, 1, ksize=3)

    # Calcul du module du gradient
    moduleGradient = np.sqrt(dI_dx**2 + dI_dy**2)

    # Seuil défini en fonction de votre image
    seuil_module = 50

    # Contour obtenu avec binarisation de l'image : si module du gradient > seuil => contour
    contours_module = (moduleGradient > seuil_module).astype(np.uint8) * 255

    return contours_module, dI_dx, dI_dy

# Fonction pour appliquer une palette de couleurs
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

# Fonction pour appliquer un flou gaussien
def appliquer_flou(image, taille_kernel=(101, 101)):
    return cv2.GaussianBlur(image, taille_kernel, 0)

# Fonction pour appliquer un flou à l'image en utilisant la décomposition en valeurs singulières (SVD)
def appliquer_svd_flou(image, k=10):
    img = image.astype(np.float64)
    canaux = cv2.split(img)  # Séparer les canaux de couleur
    canaux_reconstruits = []
    for canal in canaux:
        U, S_diag, VT = np.linalg.svd(canal, full_matrices=False)
        k = min(k, len(S_diag))
        S_diag_k = np.zeros_like(S_diag)
        S_diag_k[:k] = S_diag[:k]
        S = np.diag(S_diag_k)
        canal_reconstruit = np.dot(U, np.dot(S, VT))
        canaux_reconstruits.append(canal_reconstruit)
    img_reconstruite = cv2.merge(canaux_reconstruits)
    img_reconstruite[img_reconstruite > 255] = 255
    img_reconstruite[img_reconstruite < 0] = 0
    img_reconstruite = img_reconstruite.astype(np.uint8)
    return img_reconstruite

def transformer_en_image_bd(image):
    # Extraire les contours en couleur
    contours_couleur = cv2.Canny(image, 30, 400)  # Utiliser Canny pour extraire les contours colorés

    # Appliquer un filtre médian pour réduire le bruit sur l'image couleur
    image_lissee = cv2.medianBlur(image, 7)  # Vous pouvez ajuster la taille du noyau

    # Appliquer la quantification des couleurs pour simplifier les couleurs de l'image
    num_colors = 8  # Vous pouvez ajuster ce nombre en fonction de vos préférences
    quantized_image = image_lissee // (256 // num_colors) * (256 // num_colors)

    # Créer une image de bande dessinée en couleur avec les contours en couleur
    image_bd_couleur = cv2.bitwise_and(quantized_image, quantized_image, mask=~contours_couleur)

    return image_bd_couleur

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

        # Bouton pour ouvrir la fenêtre Tkinter
        startButton = QPushButton("Start", self)
        startButton.clicked.connect(self.openTkinterWindow)
        vbox.addWidget(startButton)

        self.setLayout(vbox)

    def openTkinterWindow(self):
        main()  # Appel de la fonction main de votre script
        self.close()  # Fermer la fenêtre de l'interface PyQt5

def main():
    # Choisir une image
    image = choisir_image()

    if image is None:
        print("Aucune image n'a été sélectionnée. Sortie du programme.")
        return

    # Créer une fenêtre Tkinter
    root = tk.Tk()
    root.title("Traitement d'images")

    # Créer un cadre pour afficher les images
    frame = ttk.Frame(root)
    frame.pack()

    # Boutons pour afficher les différentes images
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

    btn_original = ttk.Button(frame, text="Image originale", command=afficher_image_original)
    btn_original.pack()

    btn_contours = ttk.Button(frame, text="Contours", command=afficher_contours)
    btn_contours.pack()

    btn_gradients = ttk.Button(frame, text="Gradients", command=afficher_gradients)
    btn_gradients.pack()

    btn_bd = ttk.Button(frame, text="Image de bande dessinée", command=afficher_bd)
    btn_bd.pack()

    btn_image_combinees = ttk.Button(frame, text="Image combinée", command=afficher_image_combinees)
    btn_image_combinees.pack()

    btn_montage_flou = ttk.Button(frame, text="Montage flou", command=afficher_montage_flou)
    btn_montage_flou.pack()

    btn_image_flou = ttk.Button(frame, text="Image flou", command=afficher_image_flou)
    btn_image_flou.pack()

    btn_montage_warhol = ttk.Button(frame, text="Montage Warhol", command=afficher_montage_warhol)
    btn_montage_warhol.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
