import tkinter as tk
# Importamos lo necesario desde la raíz (asumiendo que ejecutas main.py)
from Logic.datos import db_personajes
from Logic.motor import estado_juego, validar_nombre, obtener_stats

# --- FUNCIONES DE INTERFAZ (Controlan lo que se ve) ---

def verificar_estado():
    """Actualiza visualmente el botón según el diccionario de motor.py"""
    if estado_juego["nombre"] and estado_juego["personaje"] and estado_juego["avatar"]:
        btn_comenzar.config(state="normal", fg="green")
    else:
        btn_comenzar.config(state="disabled", fg="gray")

def mostrar_frame(frame_objetivo):
    """Navegación entre capas."""
    frame_menu.pack_forget()
    frame_chsel.pack_forget()
    frame_avatar.pack_forget()
    frame_objetivo.pack(fill="both", expand=True)

def confirmar_nombre(*args):
    """Usa la lógica de motor.py para validar el input del usuario."""
    nombre_ingresado = var_nombre.get()
    if validar_nombre(nombre_ingresado):
        estado_juego["nombre"] = True
    else:
        estado_juego["nombre"] = False
    verificar_estado()

def confirmar_seleccion_pj():
    """Extrae la selección de la lista y actualiza el motor."""
    seleccion = lista_pj.curselection()
    if seleccion:
        nombre_pj = lista_pj.get(seleccion)
        estado_juego["personaje"] = True
        estado_juego["stats"] = obtener_stats(nombre_pj)
        
        print(f"PJ: {nombre_pj} | Stats: {estado_juego['stats']}")
        verificar_estado()
        mostrar_frame(frame_menu)

def temp_seleccionar_av():
    """Simulación de selección de avatar."""
    estado_juego["avatar"] = True 
    verificar_estado()
    mostrar_frame(frame_menu)

# --- CONFIGURACIÓN DE UI (Widgets) ---

ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("450x550")

var_nombre = tk.StringVar()
var_nombre.trace_add("write", confirmar_nombre)

# Frames
frame_menu = tk.Frame(ventana_principal)
frame_chsel = tk.Frame(ventana_principal)
frame_avatar = tk.Frame(ventana_principal)

# --- PANTALLA: MENÚ PRINCIPAL ---
frame_menu.pack(fill="both", expand=True)
tk.Label(frame_menu, text="Epic Adventure", font=("Consolas", 16, "bold")).pack(pady=20)
tk.Label(frame_menu, text="NOMBRE DEL JUGADOR:", font=("Consolas", 10)).pack()
tk.Entry(frame_menu, textvariable=var_nombre, font=("Consolas", 11), justify="center").pack(pady=5)

btn_comenzar = tk.Button(frame_menu, text="COMENZAR JUEGO", state="disabled", font=("Consolas", 11, "bold"))
btn_comenzar.pack(pady=15)

tk.Button(frame_menu, text="[ SELECCIONAR PERSONAJE ]", font=("Consolas", 10),
          command=lambda: mostrar_frame(frame_chsel)).pack(pady=5)
tk.Button(frame_menu, text="[ SELECCIONAR AVATAR ]", font=("Consolas", 10),
          command=lambda: mostrar_frame(frame_avatar)).pack(pady=5)

# --- PANTALLA: SELECCIÓN PERSONAJE ---
tk.Label(frame_chsel, text="--- SELECCIÓN DE LUCHADOR ---", font=("Consolas", 12, "bold")).pack(pady=20)
frame_lista = tk.Frame(frame_chsel)
frame_lista.pack(pady=10)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side="right", fill="y")

lista_pj = tk.Listbox(frame_lista, font=("Consolas", 11), height=10, width=30, yscrollcommand=scrollbar.set)

# Poblamos usando las llaves de datos.py (importado al inicio)
for p in db_personajes.keys():
    lista_pj.insert("end", p)

lista_pj.pack(side="left")
scrollbar.config(command=lista_pj.yview)

tk.Button(frame_chsel, text="GUARDAR Y VOLVER", font=("Consolas", 10, "bold"),
          bg="#e1e1e1", command=confirmar_seleccion_pj).pack(pady=20)

# --- PANTALLA: SELECCIÓN AVATAR ---
tk.Label(frame_avatar, text="--- INTERFAZ AVATAR ---", font=("Consolas", 12, "bold")).pack(pady=20)
tk.Button(frame_avatar, text="GUARDAR Y VOLVER", font=("Consolas", 10, "bold"),
          command=temp_seleccionar_av).pack(pady=20)