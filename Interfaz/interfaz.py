import tkinter as tk
import os
from Logic.datos import db_personajes, lista_avatares, tierras_hollows, coordenadas_tierras
from Logic.motor import estado_juego, validar_nombre, obtener_stats, asignar_avatar

# --- VARIABLES GLOBALES Y DE CONTROL ---
img_fondo_mapa = None 
img_fondo_menu = None 
img_fondo_chsel = None  
img_fondo_avatar = None 
seleccionados_actualmente = [] 
botones_pj = {} 

# --- INICIALIZACIÓN ---
ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("450x550") 

var_nombre = tk.StringVar()

# --- FRAMES ---
frame_menu = tk.Frame(ventana_principal)
frame_chsel = tk.Frame(ventana_principal)
frame_avatar = tk.Frame(ventana_principal)
frame_about = tk.Frame(ventana_principal)
frame_mapa = tk.Frame(ventana_principal)

def mostrar_frame(frame_objetivo):
    """Oculta todos los frames y muestra el seleccionado."""
    for f in [frame_menu, frame_chsel, frame_avatar, frame_about, frame_mapa]:
        f.pack_forget()
    frame_objetivo.pack(fill="both", expand=True)

# --- LÓGICA DE SELECCIÓN DE PERSONAJES ---

def seleccionar_personaje_grid(nombre):
    """Maneja la selección de 3 personajes con feedback visual."""
    global seleccionados_actualmente
    boton = botones_pj[nombre]

    if nombre in seleccionados_actualmente:
        seleccionados_actualmente.remove(nombre)
        boton.config(bg="SystemButtonFace", relief="raised")
    else:
        if len(seleccionados_actualmente) < 3:
            seleccionados_actualmente.append(nombre)
            boton.config(bg="#2ecc71", relief="sunken")
        else:
            print("Ya tienes 3 personajes")
    
    verificar_estado_seleccion()

def verificar_estado_seleccion():
    """Habilita el botón de guardar solo con 3 elegidos."""
    if len(seleccionados_actualmente) == 3:
        btn_guardar_pj.config(state="normal", bg="#2ecc71", fg="white")
    else:
        btn_guardar_pj.config(state="disabled", bg="gray", fg="black")

def guardar_seleccion_final():
    """Guarda en el motor y vuelve al menú."""
    estado_juego["personajes_elegidos"] = [obtener_stats(n) for n in seleccionados_actualmente]
    verificar_estado() 
    mostrar_frame(frame_menu)

def refrescar_pantalla_seleccion():
    """Selección de personajes con fondo y cuadrícula."""
    global btn_guardar_pj, img_fondo_chsel
    for widget in frame_chsel.winfo_children():
        widget.destroy()
        
    ventana_principal.geometry("1024x768")
    canvas_chsel = tk.Canvas(frame_chsel, width=1024, height=768, highlightthickness=0)
    canvas_chsel.pack(fill="both", expand=True)
    
    dir_actual = os.path.dirname(__file__)
    ruta_fondo = os.path.join(dir_actual, "Assets", "fondo_personajes.png")
    
    try:
        img_fondo_chsel = tk.PhotoImage(file=ruta_fondo)
        canvas_chsel.create_image(0, 0, image=img_fondo_chsel, anchor="nw")
    except:
        canvas_chsel.config(bg="#0f0f0f")

    lbl_titulo = tk.Label(frame_chsel, text="--- SELECCIONA TU EQUIPO ---", 
                          font=("Consolas", 18, "bold"), bg="#1a1a1a", fg="white")
    canvas_chsel.create_window(512, 40, window=lbl_titulo)

    contenedor_grid = tk.Frame(frame_chsel, bg="#1a1a1a")
    canvas_chsel.create_window(512, 380, window=contenedor_grid)

    fila, columna = 0, 0
    for nombre in db_personajes.keys():
        cajita = tk.Frame(contenedor_grid, width=140, height=190, bg="#1a1a1a")
        cajita.grid(row=fila, column=columna, padx=8, pady=8)
        cajita.pack_propagate(False) 

        img_tk = None
        try:
            ruta_pj = os.path.join(dir_actual, "Assets", db_personajes[nombre]["img"])
            raw_img = tk.PhotoImage(file=ruta_pj)
            img_tk = raw_img.subsample(1, 1) 
            db_personajes[nombre]["_tk"] = img_tk 
        except: img_tk = None

        btn = tk.Button(cajita, image=img_tk, relief="raised",
                        command=lambda n=nombre: seleccionar_personaje_grid(n))
        btn.pack(side="top", fill="both", expand=True)
        botones_pj[nombre] = btn

        tipo = db_personajes[nombre].get("tipo", "N/A")
        tk.Label(cajita, text=f"{nombre}\n({tipo})", font=("Consolas", 8, "bold"), 
                 bg="#1a1a1a", fg="white", wraplength=130).pack(side="bottom", fill="x")

        if nombre in seleccionados_actualmente:
            btn.config(bg="#2ecc71", relief="sunken")

        columna += 1
        if columna > 4: columna, fila = 0, fila + 1

    btn_guardar_pj = tk.Button(frame_chsel, text="CONFIRMAR EQUIPO", state="disabled",
                               font=("Consolas", 12, "bold"), command=guardar_seleccion_final)
    canvas_chsel.create_window(512, 720, window=btn_guardar_pj)
    mostrar_frame(frame_chsel)

# --- SELECCIÓN DE AVATAR (ESTILO PERSONAJES) ---

def mostrar_seleccion_avatar():
    """Muestra la selección de avatar con fondo, imágenes y texto abajo."""
    global img_fondo_avatar
    for widget in frame_avatar.winfo_children():
        widget.destroy()
    
    ventana_principal.geometry("600x650")
    canvas_av = tk.Canvas(frame_avatar, width=600, height=650, highlightthickness=0)
    canvas_av.pack(fill="both", expand=True)
    
    dir_actual = os.path.dirname(__file__)
    ruta_fondo = os.path.join(dir_actual, "Assets", "fondo_avatar.png")
    
    try:
        img_fondo_avatar = tk.PhotoImage(file=ruta_fondo)
        canvas_av.create_image(0, 0, image=img_fondo_avatar, anchor="nw")
    except:
        canvas_av.config(bg="#1a1a1a")

    lbl_titulo = tk.Label(frame_avatar, text="--- ELIGE TU AVATAR ---", 
                          font=("Consolas", 16, "bold"), bg="#1a1a1a", fg="white")
    canvas_av.create_window(300, 40, window=lbl_titulo)

    contenedor_iconos = tk.Frame(frame_avatar, bg="#1a1a1a")
    canvas_av.create_window(300, 300, window=contenedor_iconos)

    f, c = 0, 0
    for avatar in lista_avatares: 
        cajita = tk.Frame(contenedor_iconos, width=120, height=150, bg="#1a1a1a")
        cajita.grid(row=f, column=c, padx=10, pady=10)
        cajita.pack_propagate(False)

        img_av_tk = None
        try:
            ruta_img = os.path.join(dir_actual, "Assets", avatar["img"])
            raw_img = tk.PhotoImage(file=ruta_img)
            img_av_tk = raw_img.subsample(1, 1) 
            avatar["_tk"] = img_av_tk 
        except: img_av_tk = None

        btn = tk.Button(cajita, image=img_av_tk, text="?" if not img_av_tk else "",
                        command=lambda a=avatar["nombre"]: seleccionar_este_avatar(a))
        btn.pack(side="top", fill="both", expand=True)

        tk.Label(cajita, text=avatar["nombre"], font=("Consolas", 9), 
                 bg="#1a1a1a", fg="white").pack(side="bottom", pady=2)

        c += 1
        if c > 3: c, f = 0, f + 1
        
    btn_volver = tk.Button(frame_avatar, text="VOLVER AL MENÚ", font=("Consolas", 10, "bold"),
                           command=lambda: mostrar_frame(frame_menu))
    canvas_av.create_window(300, 600, window=btn_volver)
    mostrar_frame(frame_avatar)

def seleccionar_este_avatar(nombre_avatar):
    asignar_avatar(nombre_avatar)
    verificar_estado()
    mostrar_frame(frame_menu)

# --- FUNCIONES DEL MAPA ---
def cargar_mapa():
    global img_fondo_mapa
    for widget in frame_mapa.winfo_children():
        widget.destroy()

    ventana_principal.geometry("1024x768")
    canvas = tk.Canvas(frame_mapa, width=1024, height=768, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    try:
        dir_actual = os.path.dirname(__file__)
        ruta_mapa = os.path.join(dir_actual, "..", "mario.png")
        img_fondo_mapa = tk.PhotoImage(file=ruta_mapa) 
        canvas.create_image(0, 0, image=img_fondo_mapa, anchor="nw")
    except Exception as e:
        canvas.config(bg="#0b0d17")
        canvas.create_text(512, 384, text=f"Falta mario.png\n{e}", fill="white")

    for i, tierra in enumerate(tierras_hollows):
        x, y = coordenadas_tierras[i]
        desbloqueado = i <= estado_juego["progreso"]
        color_pnt = "#5dade2" if desbloqueado else "#2c3e50"
        
        btn = tk.Button(frame_mapa, text="🪐", font=("Arial", 20, "bold"),
                        bg=color_pnt, fg="white", state="normal" if desbloqueado else "disabled",
                        command=lambda n=i: preparar_batalla(n))
        
        canvas.create_window(x, y, window=btn)
        canvas.create_text(x, y+50, text=tierra, fill="white", font=("Consolas", 10, "bold"))

    mostrar_frame(frame_mapa)

def preparar_batalla(nivel_index):
    print(f"Entrando a la batalla en el nivel {nivel_index + 1}")

# --- LÓGICA DE CONTROL GLOBAL ---
def verificar_estado():
    equipo_listo = len(estado_juego.get("personajes_elegidos", [])) == 3
    if estado_juego["nombre"] and equipo_listo and estado_juego["avatar"]:
        btn_comenzar.config(state="normal", fg="green")
    else:
        btn_comenzar.config(state="disabled", fg="gray")

def confirmar_nombre(*args):
    nombre_ingresado = var_nombre.get()
    estado_juego["nombre"] = validar_nombre(nombre_ingresado)
    verificar_estado()

var_nombre.trace_add("write", confirmar_nombre)

# --- DISEÑO: MENÚ PRINCIPAL ---
frame_menu.pack(fill="both", expand=True)
canvas_menu = tk.Canvas(frame_menu, width=450, height=550, highlightthickness=0)
canvas_menu.pack(fill="both", expand=True)

dir_actual = os.path.dirname(__file__)
ruta_fondo_menu = os.path.join(dir_actual, "Assets", "fondo_menu.png")

try:
    img_fondo_menu = tk.PhotoImage(file=ruta_fondo_menu)
    canvas_menu.create_image(0, 0, image=img_fondo_menu, anchor="nw")
except:
    canvas_menu.config(bg="#1a1a1a")

lbl_titulo = tk.Label(frame_menu, text="Epic Adventure", font=("Consolas", 20, "bold"), bg="#1a1a1a", fg="white")
canvas_menu.create_window(225, 50, window=lbl_titulo)

lbl_nombre = tk.Label(frame_menu, text="NOMBRE DEL JUGADOR:", font=("Consolas", 10, "bold"), bg="#1a1a1a", fg="white")
canvas_menu.create_window(225, 120, window=lbl_nombre)

entry_nombre = tk.Entry(frame_menu, textvariable=var_nombre, font=("Consolas", 12), justify="center", width=25)
canvas_menu.create_window(225, 150, window=entry_nombre)

global btn_comenzar 
btn_comenzar = tk.Button(frame_menu, text="COMENZAR JUEGO", state="disabled", font=("Consolas", 12, "bold"), command=cargar_mapa)
canvas_menu.create_window(225, 210, window=btn_comenzar)

btn_sel_pj = tk.Button(frame_menu, text="[ SELECCIONAR EQUIPO ]", font=("Consolas", 10), command=refrescar_pantalla_seleccion)
canvas_menu.create_window(225, 300, window=btn_sel_pj)

btn_sel_av = tk.Button(frame_menu, text="[ SELECCIONAR AVATAR ]", font=("Consolas", 10), command=mostrar_seleccion_avatar)
canvas_menu.create_window(225, 340, window=btn_sel_av)

btn_about = tk.Button(frame_menu, text="[ ACERCA DE ]", font=("Consolas", 10), command=lambda: mostrar_frame(frame_about))
canvas_menu.create_window(225, 380, window=btn_about)

# --- DISEÑO: ABOUT ---
tk.Label(frame_about, text="--- ACERCA DEL JUEGO ---", font=("Consolas", 12, "bold")).pack(pady=20)
tk.Label(frame_about, text="Epic Adventure v1.0\nTEC - Cartago", font=("Consolas", 10)).pack(pady=10)
tk.Button(frame_about, text="VOLVER", command=lambda: mostrar_frame(frame_menu)).pack(pady=10)

ventana_principal.mainloop()