import tkinter as tk
from Interfaz.main_window import InterfazJuego
from Logic.audio import reproducir_musica, detener_musica

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazJuego(root)
    reproducir_musica("menu.wav")
    app.mostrar_menu()
    root.mainloop() 
    detener_musica()