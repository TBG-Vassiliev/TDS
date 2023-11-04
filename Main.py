import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

def button_clicked():
    print("Bouton cliqué")

root = tk.Tk()
root.title("Boutons esthétiques")

style = ThemedStyle(root)
style.set_theme("adapta")  # Choisissez un thème parmi ceux disponibles

button1 = ttk.Button(root, text="Bouton 1", command=button_clicked)
button1.pack()

button2 = ttk.Button(root, text="Bouton 2", command=button_clicked)
button2.pack()

button3 = ttk.Button(root, text="Bouton 3", command=button_clicked)
button3.pack()

button4 = ttk.Button(root, text="Bouton 4", command=button_clicked)
button4.pack()

button5 = ttk.Button(root, text="Bouton 5", command=button_clicked)
button5.pack()

root.mainloop()
