import tkinter as tk
from Interfaz.pantalla_menu import crear_pantalla_menu
from Interfaz.pantalla_seleccion import refrescar_pantalla_seleccion
from Interfaz.pantalla_avatar import crear_pantalla_avatar
from Interfaz.pantalla_about import crear_pantalla_about
from Interfaz.pantalla_mapa import crear_pantalla_mapa
from Logic.motor import estado_juego, validar_nombre

class InterfazJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("EPIC ADVENTURE")
        self.root.geometry("1280x720")
        self.var_nombre = tk.StringVar()
        self.var_nombre.trace_add("write", self.confirmar_nombre)
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)
        self.btn_comenzar = None
        self.canvas_menu = None

    def limpiar_pantalla_recursiva(self, widgets):
        if not widgets:
            return
        widgets[0].destroy()
        self.limpiar_pantalla_recursiva(widgets[1:])

    def mostrar_menu(self):
        self.limpiar_pantalla_recursiva(self.contenedor.winfo_children())
        self.canvas_menu = crear_pantalla_menu(
            self.contenedor, 
            self.ir_a_seleccion, 
            self.ir_a_avatar, 
            self.ir_a_about,
            self.var_nombre
        )
        
        self.btn_comenzar = tk.Button(
            self.contenedor, 
            text="COMENZAR JUEGO", 
            state="disabled",
            font=("Consolas", 18, "bold"),
            command=self.ir_a_mapa
        )
        self.canvas_menu.create_window(640, 380, window=self.btn_comenzar)
        
        self.verificar_estado_general()

    def confirmar_nombre(self, *args):
        nombre_raw = self.var_nombre.get()
        estado_juego["nombre"] = validar_nombre(nombre_raw)
        self.verificar_estado_general()

    def verificar_estado_recursivo(self, checks):
        if not checks:
            return True
        if not checks[0]:
            return False
        return self.verificar_estado_recursivo(checks[1:])

    def verificar_estado_general(self):
        if self.btn_comenzar and self.btn_comenzar.winfo_exists():
            equipo = estado_juego.get("personajes_elegidos", [])
            
            condiciones = [
                bool(estado_juego.get("nombre")),
                len(equipo) == 3,
                bool(estado_juego.get("avatar"))
            ]
            
            if self.verificar_estado_recursivo(condiciones):
                self.btn_comenzar.config(state="normal", fg="#2ecc71")
            else:
                self.btn_comenzar.config(state="disabled", fg="gray")

    def ir_a_seleccion(self):
        refrescar_pantalla_seleccion(self.contenedor, self.mostrar_menu)

    def ir_a_avatar(self):
        crear_pantalla_avatar(self.contenedor, self.mostrar_menu)

    def ir_a_about(self):
        crear_pantalla_about(self.contenedor, self.mostrar_menu)

    def ir_a_mapa(self):
        crear_pantalla_mapa(self.contenedor, estado_juego, self.iniciar_batalla)

    def iniciar_batalla(self, nivel_index):
        print(f"DEBUG: Iniciando nivel {nivel_index}...")