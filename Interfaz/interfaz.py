import tkinter as tk

def abrir_ChSel():
    ventana_principal.withdraw()
    ChSel = tk.Toplevel()
    ChSel.title("SELECCIÓN PERSONAJE")
    ChSel.geometry("400x300")
    ChSel.protocol("WM_DELETE_WINDOW", lambda: cerrar_seleccion(ChSel))
    
    tk.Label(ChSel, text="Seleccione su personaje", font=("Consolas", 12)).pack(pady=20)

def cerrar_ChSel(ventana_secundaria):
    ventana_secundaria.destroy()
    ventana_principal.deiconify() 


ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("400x300")

tk.Label(ventana_principal, text="Epic Adventure", font=("Consolas", 14, "bold")).pack(pady=10)


boton = tk.Button(ventana_principal, text="JUGAR", command=abrir_ChSel)
boton.pack(pady=20)

ventana_principal.mainloop()