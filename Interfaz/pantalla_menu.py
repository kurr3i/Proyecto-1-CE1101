# ==========================================
# INTERFAZ: PANTALLA PRINCIPAL DE MENÚ
# ==========================================
import tkinter as tk
from Interfaz.componentes import cargar_img

# ==========================================
# UTILIDADES DE INTERFAZ
# ==========================================
def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

# ==========================================
# RENDERIZADO DE PANTALLA
# ==========================================
def crear_pantalla_menu(frame_padre, ir_a_chsel, ir_a_avatar, ir_a_about, var_nombre):
    limpiar_widgets_recursivo(frame_padre.winfo_children())
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    frame_padre.img_fondo = cargar_img("fondo_menu.png")
    if frame_padre.img_fondo:
        canvas.create_image(0, 0, image=frame_padre.img_fondo, anchor="nw")

    canvas.create_text(640, 120, text="Epic Adventure", font=("Consolas", 45, "bold"), fill="white")

    entry = tk.Entry(frame_padre, textvariable=var_nombre, font=("Consolas", 18), justify="center")
    canvas.create_window(640, 280, window=entry)

    btn_equipo = tk.Button(frame_padre, text="[ SELECCIONAR EQUIPO ]", command=ir_a_chsel)
    canvas.create_window(640, 480, window=btn_equipo)

    btn_avatar = tk.Button(frame_padre, text="[ SELECCIONAR AVATAR ]", command=ir_a_avatar)
    canvas.create_window(640, 540, window=btn_avatar)

    btn_about = tk.Button(frame_padre, text="[ ACERCA DE ]", command=ir_a_about)
    canvas.create_window(640, 600, window=btn_about)
    
    return canvas