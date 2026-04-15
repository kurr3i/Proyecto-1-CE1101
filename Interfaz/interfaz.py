import tkinter as tk
import os
from Logic.datos import db_personajes, lista_avatares, tierras_hollows, coordenadas_tierras
from Logic.motor import estado_juego, validar_nombre, obtener_stats, asignar_avatar

# --- VARIABLE GLOBAL PARA LA IMAGEN ---
img_fondo_mapa = None 

# --- INICIALIZACIÓN DE VENTANA Y VARIABLES ---
ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("450x550") # Tamaño inicial del menú

var_nombre = tk.StringVar()

# --- DECLARACIÓN DE FRAMES ---
frame_menu = tk.Frame(ventana_principal)
frame_chsel = tk.Frame(ventana_principal)
frame_avatar = tk.Frame(ventana_principal)
frame_about = tk.Frame(ventana_principal)
frame_mapa = tk.Frame(ventana_principal)

# --- LÓGICA DE NAVEGACIÓN ---
def mostrar_frame(frame_objetivo):
    """Oculta todos los frames y muestra el seleccionado."""
    for f in [frame_menu, frame_chsel, frame_avatar, frame_about, frame_mapa]:
        f.pack_forget()
    frame_objetivo.pack(fill="both", expand=True)

# --- FUNCIONES DEL MAPA (ID 01) ---
def cargar_mapa():
    global img_fondo_mapa
    
    # Limpiamos el frame
    for widget in frame_mapa.winfo_children():
        widget.destroy()

    # Ajustamos ventana a la resolución de tu imagen
    ventana_principal.geometry("1024x768")
    
    # Creamos el Canvas
    canvas = tk.Canvas(frame_mapa, width=1024, height=768, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Intentamos cargar la imagen de Mario
    try:
        # Esto obtiene la ruta de la carpeta donde vive interfaz.py
        directorio_actual = os.path.dirname(__file__)
        
        # Si la imagen está un nivel arriba de Interfaz/
        # usamos '..' para subir una carpeta
        ruta_imagen = os.path.join(directorio_actual, "..", "mario.png")
        
        img_fondo_mapa = tk.PhotoImage(file=ruta_imagen) 
        canvas.create_image(0, 0, image=img_fondo_mapa, anchor="nw")
    except Exception as e:
        canvas.config(bg="#0b0d17")
        canvas.create_text(512, 384, text=f"Error: No se halló mario.png\n{e}", fill="white")

    # Dibujar los planetas sobre la imagen
    for i, tierra in enumerate(tierras_hollows):
        x, y = coordenadas_tierras[i]
        
        desbloqueado = i <= estado_juego["progreso"]
        color_pnt = "#5dade2" if desbloqueado else "#2c3e50"
        
        btn = tk.Button(frame_mapa, 
                        text="🪐", 
                        font=("Arial", 20, "bold"),
                        bg=color_pnt, 
                        fg="white",
                        activebackground="#2980b9",
                        bd=2,
                        state="normal" if desbloqueado else "disabled",
                        command=lambda n=i: preparar_batalla(n))
        
        canvas.create_window(x, y, window=btn)
        canvas.create_text(x, y+50, text=tierra, fill="white", font=("Consolas", 10, "bold"))

    mostrar_frame(frame_mapa)

def preparar_batalla(nivel_index):
    print(f"Entrando a la batalla en el nivel {nivel_index + 1}")

# --- LÓGICA DE CONTROL (ID 00) ---
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

def confirmar_seleccion_pj():
    indices = lista_pj.curselection()
    if len(indices) == 3:
        nombres = [lista_pj.get(i) for i in indices]
        estado_juego["personajes_elegidos"] = [obtener_stats(n) for n in nombres]
        verificar_estado() 
        mostrar_frame(frame_menu)
    else:
        print("Error: Selecciona 3 personajes")

def seleccionar_este_avatar(icono):
    asignar_avatar(icono)
    verificar_estado()
    mostrar_frame(frame_menu)

# --- DISEÑO: MENÚ PRINCIPAL ---
frame_menu.pack(fill="both", expand=True)
tk.Label(frame_menu, text="Epic Adventure", font=("Consolas", 16, "bold")).pack(pady=20)
tk.Label(frame_menu, text="NOMBRE DEL JUGADOR:", font=("Consolas", 10)).pack()
tk.Entry(frame_menu, textvariable=var_nombre, font=("Consolas", 11), justify="center").pack(pady=5)

btn_comenzar = tk.Button(frame_menu, text="COMENZAR JUEGO", state="disabled", 
                         font=("Consolas", 11, "bold"), command=cargar_mapa)
btn_comenzar.pack(pady=15)

tk.Button(frame_menu, text="[ SELECCIONAR PERSONAJE ]", font=("Consolas", 10), 
          command=lambda: mostrar_frame(frame_chsel)).pack(pady=5)
tk.Button(frame_menu, text="[ SELECCIONAR AVATAR ]", font=("Consolas", 10), 
          command=lambda: mostrar_frame(frame_avatar)).pack(pady=5)

# --- DISEÑO: SELECCIÓN PERSONAJE ---
tk.Label(frame_chsel, text="--- SELECCIÓN DE LUCHADOR ---", font=("Consolas", 12, "bold")).pack(pady=20)
frame_lista = tk.Frame(frame_chsel)
frame_lista.pack(pady=10)
scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side="right", fill="y")
lista_pj = tk.Listbox(frame_lista, font=("Consolas", 11), height=10, width=30, 
                      yscrollcommand=scrollbar.set, selectmode="multiple")
for p in db_personajes.keys():
    lista_pj.insert("end", p)
lista_pj.pack(side="left")
scrollbar.config(command=lista_pj.yview)
tk.Button(frame_chsel, text="GUARDAR Y VOLVER", command=confirmar_seleccion_pj).pack(pady=20)

# --- DISEÑO: SELECCIÓN AVATAR ---
tk.Label(frame_avatar, text="--- SELECCIONA TU AVATAR ---", font=("Consolas", 12, "bold")).pack(pady=20)
contenedor_iconos = tk.Frame(frame_avatar)
contenedor_iconos.pack(pady=10)
f, c = 0, 0
for icono in lista_avatares:
    btn = tk.Button(contenedor_iconos, text=icono, font=("Segoe UI Emoji", 20), 
                    command=lambda i=icono: seleccionar_este_avatar(i))
    btn.grid(row=f, column=c, padx=5, pady=5)
    c += 1
    if c > 3: c, f = 0, f + 1
tk.Button(frame_avatar, text="CANCELAR", command=lambda: mostrar_frame(frame_menu)).pack(pady=20)

# --- DISEÑO: ABOUT ---
tk.Label(frame_about, text="--- ACERCA DEL JUEGO ---", font=("Consolas", 12, "bold")).pack(pady=20)
tk.Label(frame_about, text="Epic Adventure v1.0\nTEC - Cartago", font=("Consolas", 10)).pack(pady=10)
tk.Button(frame_about, text="VOLVER", command=lambda: mostrar_frame(frame_menu)).pack(pady=10)

ventana_principal.mainloop()