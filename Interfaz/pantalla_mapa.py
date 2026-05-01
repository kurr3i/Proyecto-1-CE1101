# ==========================================
# INTERFAZ: PANTALLA DE MAPA (NIVELES Y HOLLOWS)
# ==========================================
import tkinter as tk
from Interfaz.componentes import cargar_img

nombres_hollows = [
    "Mustafar",
    "El Castillo de la Princesa Peach",
    "El Templo del Tiempo",
    "Chepe Centro",
    "La Unión Multiversal"
]

def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

def crear_pantalla_mapa(frame_padre, estado_juego, callback_batalla):
    limpiar_widgets_recursivo(frame_padre.winfo_children())
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.refs = {}
    
    img_fondo = cargar_img("mario.png")
    if img_fondo:
        canvas.refs["bg"] = img_fondo
        canvas.create_image(0, 0, image=img_fondo, anchor="nw")
        
    progreso = estado_juego.get("progreso", 0)
    
    canvas.create_text(640, 80, text="SELECCIONA TU PRÓXIMO OBJETIVO", font=("Consolas", 35, "bold"), fill="#f1c40f")
    
    generar_nodos_recursivo(canvas, frame_padre, progreso, callback_batalla, 0)

# ==========================================
# GENERACIÓN DINÁMICA DE NODOS
# ==========================================
def generar_nodos_recursivo(canvas, frame_padre, progreso, callback_batalla, indice):
    if indice >= 5:
        return
    
    x_pos = 200 + (indice * 220)
    y_pos = 360 if indice % 2 == 0 else 480
    nombre_nivel = nombres_hollows[indice]
    
    if indice < progreso:
        color_btn = "#2ecc71"
        texto_btn = "COMPLETADO"
        estado_btn = "disabled"
    elif indice == progreso:
        color_btn = "#e74c3c"
        texto_btn = "ATACAR"
        estado_btn = "normal"
    else:
        color_btn = "#7f8c8d"
        texto_btn = "BLOQUEADO"
        estado_btn = "disabled"
        
    canvas.create_text(x_pos, y_pos - 90, text=nombre_nivel, font=("Consolas", 14, "bold"), 
                       fill="white", width=200, justify="center")
    
    img_hollow = cargar_img(f"hollow_{indice}.png")
    if img_hollow:
        canvas.refs[f"h_{indice}"] = img_hollow
        canvas.create_image(x_pos, y_pos - 150, image=img_hollow)
        
    btn = tk.Button(frame_padre, text=texto_btn, font=("Consolas", 12, "bold"), bg=color_btn, fg="white",
                    state=estado_btn, width=12, command=lambda i=indice: callback_batalla(i))
    canvas.create_window(x_pos, y_pos, window=btn)
    
    if indice < 4:
        next_x = 200 + ((indice + 1) * 220)
        next_y = 360 if (indice + 1) % 2 == 0 else 480
        color_linea = "#f1c40f" if indice < progreso else "#7f8c8d"
        canvas.create_line(x_pos + 60, y_pos, next_x - 60, next_y, fill=color_linea, width=4, dash=(10, 5))
                           
    generar_nodos_recursivo(canvas, frame_padre, progreso, callback_batalla, indice + 1)