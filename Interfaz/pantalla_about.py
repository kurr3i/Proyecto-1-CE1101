# ==========================================
# INTERFAZ: PANTALLA ACERCA DE (ABOUT)
# ==========================================
import tkinter as tk
from Interfaz.componentes import cargar_img

def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

def crear_pantalla_about(frame_padre, callback_volver):
    limpiar_widgets_recursivo(frame_padre.winfo_children())
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, bg="#0a0a0a", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    img_fondo = cargar_img("fondo_about.png")
    if img_fondo:
        canvas.bg_ref = img_fondo
        canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    
    canvas.create_text(640, 150, text="ACERCA DE EPIC ADVENTURE", font=("Consolas", 45, "bold"), fill="#f1c40f")
    canvas.create_text(640, 300, text="Desarrollador: Joshua Andrade", font=("Consolas", 24, "bold"), fill="white")
    canvas.create_text(640, 360, text="Ingeniería en Computación - Proyecto en Python puro (Tkinter)", font=("Consolas", 18, "italic"), fill="#bdc3c7")
    canvas.create_text(640, 420, text="Sistema de combate táctico y motor de renderizado customizado.", font=("Consolas", 16), fill="#7f8c8d")
    
    btn_volver = tk.Button(frame_padre, text="VOLVER AL MENÚ", font=("Consolas", 16, "bold"),
                           bg="#e74c3c", fg="white", width=20, pady=5, command=callback_volver)
    canvas.create_window(640, 600, window=btn_volver)