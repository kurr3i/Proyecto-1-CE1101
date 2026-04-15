import tkinter as tk

ventana_principal = tk.Tk()
ventana_principal.title("EPIC ADVENTURE")
ventana_principal.geometry("400x300")

estado_juego = {
    "nombre": False,
    "personaje": False,
    "avatar": False
}

def verificar_estado():
    if all(estado_juego.values()):
        btn_comenzar.config(state="normal", fg="green")
    else:
        btn_comenzar.config(state="disabled", fg="gray")

def mostrar_frame(frame_objetivo):
    frame_menu.pack_forget()
    frame_chsel.pack_forget()
    frame_avatar.pack_forget()
    frame_objetivo.pack(fill="both", expand=True)

def confirmar_nombre(*args):
    if len(var_nombre.get().strip()) >= 3:
        estado_juego["nombre"] = True
    else:
        estado_juego["nombre"] = False
    verificar_estado()

var_nombre = tk.StringVar()
var_nombre.trace_add("write", confirmar_nombre)


frame_menu = tk.Frame(ventana_principal)
frame_chsel = tk.Frame(ventana_principal)
frame_avatar = tk.Frame(ventana_principal)


frame_menu.pack(fill="both", expand=True)

tk.Label(frame_menu, text="Epic Adventure", font=("Consolas", 14, "bold")).pack(pady=10)

tk.Label(frame_menu, text="NOMBRE DEL JUGADOR:", font=("Consolas", 10)).pack()
tk.Entry(frame_menu, textvariable=var_nombre, font=("Consolas", 11), justify="center").pack(pady=5)

btn_comenzar = tk.Button(frame_menu, text="COMENZAR JUEGO", state="disabled", font=("Consolas", 10, "bold"))
btn_comenzar.pack(pady=10)

btn_ir_chsel = tk.Button(frame_menu, text="SELECCIONAR PERSONAJE", 
                         command=lambda: mostrar_frame(frame_chsel))
btn_ir_chsel.pack(pady=5)

btn_ir_avatar = tk.Button(frame_menu, text="SELECCIONAR AVATAR", 
                          command=lambda: mostrar_frame(frame_avatar))
btn_ir_avatar.pack(pady=5)



tk.Label(frame_chsel, text="--- INTERFAZ PERSONAJE ---", font=("Consolas", 12)).pack(pady=20)
tk.Label(frame_chsel, text="15 PERSONAJES", fg="blue").pack(pady=10)

def temp_seleccionar_pj():
    estado_juego["personaje"] = True
    verificar_estado()
    mostrar_frame(frame_menu)

tk.Button(frame_chsel, text="GUARDAR Y VOLVER", command=temp_seleccionar_pj).pack(pady=20)



tk.Label(frame_avatar, text="--- INTERFAZ AVATAR ---", font=("Consolas", 12)).pack(pady=20)
tk.Label(frame_avatar, text="AVATAR", fg="purple").pack(pady=10)

def temp_seleccionar_av():
    estado_juego["avatar"] = True 
    verificar_estado()
    mostrar_frame(frame_menu)

tk.Button(frame_avatar, text="GUARDAR Y VOLVER", command=temp_seleccionar_av).pack(pady=20)

ventana_principal.mainloop()