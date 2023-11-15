import cv2
import os
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Liste des caractères ASCII utilisés pour la conversion d'image en code ASCII
ASCII_CHARS = "@%#*+=-:.0123456789 "

# Redimensionne l'image en fonction de la nouvelle largeur
def redimensionner_image(image, nouvelle_largeur=100):
    largeur, hauteur = image.size
    ratio = hauteur / float(largeur / nouvelle_largeur)
    nouvelle_hauteur = int(hauteur / ratio)
    nouvelle_image = image.resize((nouvelle_largeur, nouvelle_hauteur))
    return nouvelle_image

# Convertit les pixels de l'image en caractères ASCII
def pixels_vers_ascii(image, echelle_gris=255):
    largeur, hauteur = image.size
    ascii_str = ""
    for y in range(hauteur):
        for x in range(largeur):
            pixel = image.getpixel((x, y))
            gris = int(0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])
            ascii_str += ASCII_CHARS[gris * (len(ASCII_CHARS) - 1) // echelle_gris]
        ascii_str += "\n"
    return ascii_str

# Configuration de la caméra et capture d'image
def capture_image_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Erreur", "Impossible d'ouvrir la webcam")
        return

    configure_camera_resolution(cap, 1280, 720)

    messagebox.showinfo("Capture d'image", "Appuyez sur 'Enter' pour capturer une image.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Erreur", "Erreur lors de la capture de l'image, essayez à nouveau.")
            continue

        cv2.imshow('Appuyez sur "Enter" pour capturer', frame)

        if cv2.waitKey(1) & 0xFF == 13:
            break

    cv2.imwrite("webcam_image.png", frame)

    image = Image.open("webcam_image.png")
    image = redimensionner_image(image)
    ascii_str = pixels_vers_ascii(image)

    with open("webcam_ascii.txt", "w") as f:
        f.write(ascii_str)
    
    cap.release()
    cv2.destroyAllWindows()

    user_response = messagebox.askyesno("Quitter l'application", "Voulez-vous quitter l'application?")
    if user_response:
        root.destroy()
    else:
        messagebox.showinfo("Succès", "Image capturée et convertie en code ASCII avec succès.")

# Fonction pour configurer la résolution de la caméra
def configure_camera_resolution(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Sélectionner un fichier image depuis le système
def choisir_image():
    chemin_image = filedialog.askopenfilename()
    return chemin_image

# Convertir une image en code ASCII et afficher le résultat
def convertir_en_ascii_et_afficher(chemin_image=None):
    if chemin_image:
        image = Image.open(chemin_image)
        image = redimensionner_image(image)
        ascii_str = pixels_vers_ascii(image)

        with open("image_importee_ascii.txt", "w") as f:
            f.write(ascii_str)

        user_response = messagebox.askyesno("Quitter l'application", "Voulez-vous quitter l'application?")
        if user_response:
            root.destroy()
        else:
            messagebox.showinfo("Succès", "Image importée convertie en code ASCII avec succès.")

# Fonction principale pour démarrer l'application
def main():
    global root
    root = tk.Tk()
    root.title("Conversion d'image en ASCII")

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10)

    webcam_button = ttk.Button(frame, text="Utiliser la Webcam", command=capture_image_webcam)
    webcam_button.grid(row=0, column=0, padx=10, pady=10)

    file_button = ttk.Button(frame, text="Importer une image depuis le fichier", command=lambda: convertir_en_ascii_et_afficher(choisir_image()))
    file_button.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()




