import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Fonction pour capturer des images de la webcam avec le filtre laplacien
def capture_image_webcam_laplacien():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Erreur", "Impossible d'ouvrir la webcam")
        return

    configure_camera_resolution(cap, 1280, 720)

    messagebox.showinfo("Capture d'image", "Appuyez sur 'Enter' pour capturer une image avec le filtre laplacien.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Erreur", "Erreur lors de la capture de l'image, essayez à nouveau.")
            continue

        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Appliquer le filtre laplacien pour détecter les contours
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian_abs = cv2.convertScaleAbs(laplacian)

        cv2.imshow('Contours Laplaciens (Webcam)', laplacian_abs)

        if cv2.waitKey(1) & 0xFF == 13:  # Appuyez sur 'Enter' pour capturer
            break

    cv2.imwrite("webcam_laplacien_image.png", laplacian_abs)
    
    cap.release()
    cv2.destroyAllWindows()

    user_response = messagebox.askyesno("Quitter l'application", "Voulez-vous quitter l'application?")
    if user_response:
        root.destroy()
    else:
        messagebox.showinfo("Succès", "Image capturée")
# Fonction pour configurer la résolution de la caméra
def configure_camera_resolution(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Fonction pour détecter les contours à partir d'un fichier image
def detecter_contours_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Charger l'image en niveaux de gris
    if image is None:
        messagebox.showerror("Erreur", "Impossible de charger l'image.")
        return

    # Appliquer le filtre laplacien pour détecter les contours
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    laplacian_abs = cv2.convertScaleAbs(laplacian)

    cv2.imshow("Contours Laplaciens (Image importée)", laplacian_abs)
    cv2.waitKey(0)

    # Sauvegarder l'image avec le filtre laplacien au format PNG
    cv2.imwrite("image_contours.png", laplacian_abs)

    cv2.destroyAllWindows()

    user_response = messagebox.askyesno("Quitter l'application", "Voulez-vous quitter l'application?")
    if user_response:
        root.destroy()
    else:
            messagebox.showinfo("Succès", "Image importée application du filtre laplacien.")

# Fonction pour choisir entre la webcam et un fichier importé
def main():
    global root
    def choisir_webcam():
        capture_image_webcam_laplacien()

    def choisir_image():
        chemin_image = filedialog.askopenfilename()
        detecter_contours_image(chemin_image)

    root = tk.Tk()
    root.title("Détection de contours avec Filtre Laplacien")

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10)

    webcam_button = ttk.Button(frame, text="Utiliser la Webcam", command=choisir_webcam)
    webcam_button.grid(row=0, column=0, padx=10, pady=10)

    file_button = ttk.Button(frame, text="Importer une image depuis le fichier", command=choisir_image)
    file_button.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
