import tkinter as tk
from Interfaz.componentes import cargar_img
from Logic.datos import tierras_hollows, coordenadas_tierras

def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

def dibujar_puntos_mapa_recursivo(canvas, frame_padre, tierras, coords, progreso, callback, i):
    if not tierras or not coords:
        return
    
    tierra = tierras[0]
    x, y = coords[0]
    
    desbloqueado = i <= progreso
    color_btn = "#5dade2" if desbloqueado else "#2c3e50"
    estado_btn = "normal" if desbloqueado else "disabled"
    
    btn = tk.Button(
        frame_padre, 
        text="🪐", 
        font=("Arial", 18, "bold"),
        bg=color_btn, 
        fg="white", 
        state=estado_btn,
        relief="flat",
        command=lambda n=i: callback(n)
    )
    
    canvas.create_window(x, y, window=btn)
    canvas.create_text(x, y + 45, text=tierra, fill="white", font=("Consolas", 10, "bold"))
    
    dibujar_puntos_mapa_recursivo(canvas, frame_padre, tierras[1:], coords[1:], progreso, callback, i + 1)

def crear_pantalla_mapa(frame_padre, estado_juego, preparar_batalla_callback):
    limpiar_widgets_recursivo(frame_padre.winfo_children())

    canvas = tk.Canvas(frame_padre, width=1280, height=720, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    img_fondo = cargar_img("mario.png") 
    if img_fondo:
        frame_padre.background_image = img_fondo 
        canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    else:
        canvas.config(bg="#0b0d17")

    progreso_actual = estado_juego.get("progreso", 0)
    
    dibujar_puntos_mapa_recursivo(
        canvas, 
        frame_padre, 
        tierras_hollows, 
        coordenadas_tierras, 
        progreso_actual, 
        preparar_batalla_callback, 
        0
    )