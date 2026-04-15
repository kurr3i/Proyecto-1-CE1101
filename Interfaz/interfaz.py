import tkinter as tk
from Logic.datos import db_personajes, lista_avatares
from Logic.motor import estado_juego, validar_nombre, obtener_stats, asignar_avatar

# --- INICIALIZACIÓN DE VENTANA Y VARIABLES ---
ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("450x550")

var_nombre = tk.StringVar()

# --- DECLARACIÓN DE FRAMES (CONTENEDORES) ---
frame_menu = tk.Frame(ventana_principal)
frame_chsel = tk.Frame(ventana_principal)
frame_avatar = tk.Frame(ventana_principal)
frame_about = tk.Frame(ventana_principal)
frame_mapa = tk.Frame(ventana_principal)

# --- LÓGICA DE NAVEGACIÓN Y CONTROL ---
def mostrar_frame(frame_objetivo):
    """Oculta todos los frames y muestra el seleccionado."""
    for f in [frame_menu, frame_chsel, frame_avatar, frame_about, frame_mapa]:
        f.pack_forget()
    frame_objetivo.pack(fill="both", expand=True)

def verificar_estado():
    """Valida los requisitos del ID 00 para habilitar el botón de inicio."""
    equipo_listo = len(estado_juego.get("personajes_elegidos", [])) == 3
    
    if estado_juego["nombre"] and equipo_listo and estado_juego["avatar"]:
        btn_comenzar.config(state="normal", fg="green")
    else:
        btn_comenzar.config(state="disabled", fg="gray")

# --- FUNCIONES DE LA PANTALLA INICIAL (ID 00) ---
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
        print(f"Equipo seleccionado: {nombres}")
        verificar_estado() 
        mostrar_frame(frame_menu)
    else:
        print("Error: Selecciona exactamente 3 personajes")

def seleccionar_este_avatar(icono):
    asignar_avatar(icono)
    print(f"Avatar seleccionado: {icono}")
    verificar_estado()
    mostrar_frame(frame_menu)

# --- FUNCIONES DEL MAPA (ID 01) ---
def cargar_mapa():
    """Dibuja el mapa y bloquea niveles según el progreso."""
    for widget in frame_mapa.winfo_children():
        widget.destroy()
        
    tk.Label(frame_mapa, text="MAPA DE FRAGMENTOS", font=("Consolas", 16, "bold")).pack(pady=20)
    
    tierras = ["Radiator Springs", "Pride Rock", "Monstropolis", "Shrek's Swamp", "Zootopia"]
    
    for i, tierra in enumerate(tierras):
        desbloqueado = i <= estado_juego["progreso"]
        estado = "normal" if desbloqueado else "disabled"
        color = "#a1e1a1" if desbloqueado else "#cccccc"
        texto = f"Nivel {i+1}: {tierra}"
        
        if i < estado_juego["progreso"]:
            texto += " ✅"

        btn = tk.Button(frame_mapa, text=texto, font=("Consolas", 11),
                        width=30, height=2, state=estado, bg=color,
                        command=lambda n=i: preparar_batalla(n))
        btn.pack(pady=10)

    tk.Button(frame_mapa, text="VOLVER AL MENÚ", command=lambda: mostrar_frame(frame_menu)).pack(pady=20)
    mostrar_frame(frame_mapa)

def preparar_batalla(nivel_index):
    print(f"Entrando a la batalla en el nivel {nivel_index + 1}")

# --- DISEÑO: MENÚ PRINCIPAL ---
frame_menu.pack(fill="both", expand=True)
tk.Label(frame_menu, text="Epic Adventure", font=("Consolas", 16, "bold")).pack(pady=20)
tk.Label(frame_menu, text="NOMBRE DEL JUGADOR:", font=("Consolas", 10)).pack()
tk.Entry(frame_menu, textvariable=var_nombre, font=("Consolas", 11), justify="center").pack(pady=5)

btn_comenzar = tk.Button(frame_menu, text="COMENZAR JUEGO", state="disabled", font=("Consolas", 11, "bold"), command=cargar_mapa)
btn_comenzar.pack(pady=15)

tk.Button(frame_menu, text="[ SELECCIONAR PERSONAJE ]", font=("Consolas", 10), command=lambda: mostrar_frame(frame_chsel)).pack(pady=5)
tk.Button(frame_menu, text="[ SELECCIONAR AVATAR ]", font=("Consolas", 10), command=lambda: mostrar_frame(frame_avatar)).pack(pady=5)
btn_about = tk.Button(frame_menu, text="?", font=("Consolas", 10, "bold"), width=2, command=lambda: mostrar_frame(frame_about))
btn_about.place(relx=0.95, rely=0.95, anchor="se")

# --- DISEÑO: SELECCIÓN PERSONAJE (ID 00) ---
tk.Label(frame_chsel, text="--- SELECCIÓN DE LUCHADOR ---", font=("Consolas", 12, "bold")).pack(pady=20)
frame_lista = tk.Frame(frame_chsel)
frame_lista.pack(pady=10)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side="right", fill="y")

lista_pj = tk.Listbox(frame_lista, font=("Consolas", 11), height=10, width=30, yscrollcommand=scrollbar.set, selectmode="multiple")
for p in db_personajes.keys():
    lista_pj.insert("end", p)
lista_pj.pack(side="left")
scrollbar.config(command=lista_pj.yview)

tk.Button(frame_chsel, text="GUARDAR Y VOLVER", font=("Consolas", 10, "bold"), bg="#e1e1e1", command=confirmar_seleccion_pj).pack(pady=20)

# --- DISEÑO: SELECCIÓN AVATAR (ID 00) ---
tk.Label(frame_avatar, text="--- SELECCIONA TU AVATAR ---", font=("Consolas", 12, "bold")).pack(pady=20)
contenedor_iconos = tk.Frame(frame_avatar)
contenedor_iconos.pack(pady=10)
fila, columna = 0, 0
for icono in lista_avatares:
    btn = tk.Button(contenedor_iconos, text=icono, font=("Segoe UI Emoji", 20), width=4, height=2, command=lambda i=icono: seleccionar_este_avatar(i))
    btn.grid(row=fila, column=columna, padx=5, pady=5)
    columna += 1
    if columna > 3:
        columna, fila = 0, fila + 1

tk.Button(frame_avatar, text="CANCELAR", command=lambda: mostrar_frame(frame_menu)).pack(pady=20)

# --- DISEÑO: ABOUT ---
tk.Label(frame_about, text="--- ACERCA DEL JUEGO ---", font=("Consolas", 12, "bold")).pack(pady=20)
info_texto = "Epic Adventure v1.0\nProyecto de Introducción a Programación"
tk.Label(frame_about, text=info_texto, font=("Consolas", 10), justify="center").pack(pady=10)
tk.Button(frame_about, text="VOLVER", command=lambda: mostrar_frame(frame_menu)).pack(pady=10)

# --- LANZAMIENTO ---
ventana_principal.mainloop()