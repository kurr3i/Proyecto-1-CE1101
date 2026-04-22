import tkinter as tk
from Interfaz.main_window import InterfazJuego

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazJuego(root)
    app.mostrar_menu()
    root.mainloop() 