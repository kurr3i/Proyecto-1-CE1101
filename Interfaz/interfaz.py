import tkinter as tk
from Logic.datos import db_personajes, lista_avatares
from Logic.motor import estado_juego, validar_nombre, obtener_stats, asignar_avatar


def verificar_estado():
    equipo_listo = len(estado_juego.get("personajes_elegidos", [])) == 3
    
    if estado_juego["nombre"] and equipo_listo and estado_juego["avatar"]:
        btn_comenzar.config(state="normal", fg="green")
    else:
        btn_comenzar.config(state="disabled", fg="gray")

def mostrar_frame(frame_objetivo):
    frame_about.pack_forget()
    frame_menu.pack_forget()
    frame_chsel.pack_forget()
    frame_avatar.pack_forget()
    frame_objetivo.pack(fill="both", expand=True)

def confirmar_nombre(*args):
    nombre_ingresado = var_nombre.get()
    if validar_nombre(nombre_ingresado):
        estado_juego["nombre"] = True
    else:
        estado_juego["nombre"] = False
    verificar_estado()

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

def temp_seleccionar_av():
    estado_juego["avatar"] = True 
    verificar_estado()
    mostrar_frame(frame_menu)
    
def seleccionar_este_avatar(icono):
    asignar_avatar(icono)
    print(f"Avatar seleccionado: {icono}")
    verificar_estado()
    mostrar_frame(frame_menu)

ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("450x550")

var_nombre = tk.StringVar()
var_nombre.trace_add("write", confirmar_nombre)

# Frames
frame_menu = tk.Frame(ventana_principal)
frame_chsel = tk.Frame(ventana_principal)
frame_avatar = tk.Frame(ventana_principal)


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
btn_about = tk.Button(frame_menu, text="?", font=("Consolas", 10, "bold"), 
                      width=2, command=lambda: mostrar_frame(frame_about))

btn_about.place(relx=0.95, rely=0.95, anchor="se")

# --- PANTALLA: SELECCIÓN PERSONAJE ---
tk.Label(frame_chsel, text="--- SELECCIÓN DE LUCHADOR ---", font=("Consolas", 12, "bold")).pack(pady=20)
frame_lista = tk.Frame(frame_chsel)
frame_lista.pack(pady=10)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side="right", fill="y")

lista_pj = tk.Listbox(frame_lista, font=("Consolas", 11), height=10, width=30, 
                      yscrollcommand=scrollbar.set, 
                      selectmode="multiple")

for p in db_personajes.keys():
    lista_pj.insert("end", p)

lista_pj.pack(side="left")
scrollbar.config(command=lista_pj.yview)

tk.Button(frame_chsel, text="GUARDAR Y VOLVER", font=("Consolas", 10, "bold"),
          bg="#e1e1e1", command=confirmar_seleccion_pj).pack(pady=20)

# --- PANTALLA: SELECCIÓN AVATAR ---
tk.Label(frame_avatar, text="--- SELECCIONA TU AVATAR ---", font=("Consolas", 12, "bold")).pack(pady=20)
contenedor_iconos = tk.Frame(frame_avatar)
contenedor_iconos.pack(pady=10)
fila = 0
columna = 0
for icono in lista_avatares:
    btn = tk.Button(contenedor_iconos, text=icono, font=("Segoe UI Emoji", 20), 
                    width=4, height=2,
                    command=lambda i=icono: seleccionar_este_avatar(i))
    btn.grid(row=fila, column=columna, padx=5, pady=5)
    
    columna += 1
    if columna > 3:
        columna = 0
        fila += 1

tk.Button(frame_avatar, text="CANCELAR", command=lambda: mostrar_frame(frame_menu)).pack(pady=20)

# --- PANTALLA: ABOUT (INFORMACIÓN) ---
frame_about = tk.Frame(ventana_principal)

tk.Label(frame_about, text="--- ACERCA DEL JUEGO ---", font=("Consolas", 12, "bold")).pack(pady=20)
info_texto = """
Epic Adventure v1.0
Proyecto de Introducción a Programación - Terminar después
"""
tk.Label(frame_about, text=info_texto, font=("Consolas", 10), justify="center").pack(pady=10)

tk.Button(frame_about, text="VOLVER", command=lambda: mostrar_frame(frame_menu)).pack(pady=10)
