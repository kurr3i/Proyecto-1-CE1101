# ==========================================
# INTERFAZ: PANTALLA DE SELECCIÓN DE AVATAR
# ==========================================
import tkinter as tk
from Interfaz.componentes import cargar_img
from Logic.datos import lista_avatares
from Logic.motor import asignar_avatar

# ==========================================
# UTILIDADES DE INTERFAZ
# ==========================================
def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

# ==========================================
# RENDERIZADO RECURSIVO DEL GRID
# ==========================================
def renderizar_avatares_recursivo(contenedor, lista, f, c):
    if not lista:
        return
    
    avatar = lista[0]
    
    cajita = tk.Frame(contenedor, width=150, height=180, bg="#1a1a1a")
    cajita.grid(row=f, column=c, padx=15, pady=15)
    cajita.pack_propagate(False)

    img_pico = cargar_img(avatar["img"])
    if img_pico:
        avatar["_tk_cache"] = img_pico 

    btn = tk.Button(cajita, image=img_pico if img_pico else "", 
                    text=avatar["nombre"] if not img_pico else "",
                    compound="top", bg="#2c3e50", fg="white",
                    command=lambda n=avatar["nombre"]: [asignar_avatar(n), contenedor.callback_volver()])
    btn.pack(fill="both", expand=True)
    
    tk.Label(cajita, text=avatar["nombre"], bg="#1a1a1a", fg="white", 
             font=("Consolas", 10, "bold")).pack()

    nuevo_c = c + 1
    nuevo_f = f
    if nuevo_c > 4:
        nuevo_c = 0
        nuevo_f = f + 1
        
    renderizar_avatares_recursivo(contenedor, lista[1:], nuevo_f, nuevo_c)

# ==========================================
# CREACIÓN DE PANTALLA
# ==========================================
def crear_pantalla_avatar(frame_padre, callback_volver):
    limpiar_widgets_recursivo(frame_padre.winfo_children())
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    img_fondo = cargar_img("fondo_avatar.png") 
    if img_fondo:
        frame_padre.img_fondo_cache = img_fondo 
        canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    else:
        canvas.config(bg="#1a1a1a")

    canvas.create_text(640, 60, text="--- SELECCIONA TU AVATAR ---", 
                       font=("Consolas", 30, "bold"), fill="#f1c40f")

    contenedor_grid = tk.Frame(frame_padre, bg="#1a1a1a", bd=2, relief="sunken")
    contenedor_grid.callback_volver = callback_volver
    canvas.create_window(640, 360, window=contenedor_grid)

    renderizar_avatares_recursivo(contenedor_grid, lista_avatares, 0, 0)

    btn_volver = tk.Button(frame_padre, text="VOLVER", font=("Consolas", 14),
                           command=callback_volver, bg="#e74c3c", fg="white")
    canvas.create_window(640, 650, window=btn_volver)