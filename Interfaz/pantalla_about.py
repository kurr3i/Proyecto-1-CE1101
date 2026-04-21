import tkinter as tk

def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

def crear_pantalla_about(frame_padre, callback_volver):
    limpiar_widgets_recursivo(frame_padre.winfo_children())
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_text(640, 200, text="--- ACERCA DEL JUEGO ---", 
                       font=("Consolas", 30, "bold"), fill="#f1c40f")
    
    info_texto = "Epic Adventure v1.0\n\nDesarrollado para:\nIntroducción a la Programación\nTEC - Cartago\n2026"
    canvas.create_text(640, 350, text=info_texto, 
                       font=("Consolas", 18), fill="white", justify="center")

    btn_volver = tk.Button(frame_padre, text="VOLVER", font=("Consolas", 14), 
                           command=callback_volver)
    canvas.create_window(640, 550, window=btn_volver)