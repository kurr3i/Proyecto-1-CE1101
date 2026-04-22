import tkinter as tk
import os
from Interfaz.pantalla_menu import crear_pantalla_menu
from Interfaz.pantalla_seleccion import refrescar_pantalla_seleccion
from Interfaz.pantalla_avatar import crear_pantalla_avatar
from Interfaz.pantalla_about import crear_pantalla_about
from Interfaz.pantalla_mapa import crear_pantalla_mapa
from Interfaz.pantalla_pelea import crear_pantalla_pelea
from Logic.motor import estado_juego, validar_nombre

class InterfazJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("EPIC ADVENTURE")
        self.root.geometry("1280x720")

        # Aquí se guarda el nombre del Entry del menú
        self.var_nombre = tk.StringVar()
        self.var_nombre.trace_add("write", self.confirmar_nombre)

        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

        self.btn_comenzar = None
        self.canvas_menu = None
        self.canvas_actual = None

    def limpiar_pantalla_recursiva(self, widgets):
        if not widgets:
            return
        widgets[0].destroy()
        self.limpiar_pantalla_recursiva(widgets[1:])

    def mostrar_menu(self):
        self.limpiar_pantalla_recursiva(self.contenedor.winfo_children())
        
        # Le pasamos self.var_nombre al menú para que el Entry escriba ahí
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
        # Mantenemos esto por si otra parte de tu código lo usa
        estado_juego["nombre"] = validar_nombre(nombre_raw)
        self.verificar_estado_general()

    # --- MÉTODOS DE NAVEGACIÓN ---
    def ir_a_seleccion(self):
        refrescar_pantalla_seleccion(self.contenedor, self.mostrar_menu)

    def ir_a_avatar(self):
        crear_pantalla_avatar(self.contenedor, self.mostrar_menu)

    def ir_a_about(self):
        crear_pantalla_about(self.contenedor, self.mostrar_menu)

    def ir_a_mapa(self):
        self.limpiar_pantalla_recursiva(self.contenedor.winfo_children())
        # Validación de los 5 niveles
        if estado_juego.get("progreso", 0) >= 5:
            self.mostrar_victoria_final()
        else:
            crear_pantalla_mapa(self.contenedor, estado_juego, self.iniciar_batalla)

    def iniciar_batalla(self, nivel_index):
        self.canvas_actual = crear_pantalla_pelea(
            self.contenedor,
            estado_juego,
            self.gestionar_fin_pelea,  
            self.gestionar_fin_pelea   
        )

    def gestionar_fin_pelea(self, *args):
        if estado_juego.get("progreso", 0) >= 5:
            self.mostrar_victoria_final()
        else:
            self.ir_a_mapa()

    # --- LÓGICA DE ESTADO ---
    def verificar_estado_general(self):
        if self.btn_comenzar and self.btn_comenzar.winfo_exists():
            equipo = estado_juego.get("personajes_elegidos", [])
            condiciones = [
                bool(self.var_nombre.get().strip()), # Verificamos directo de la variable
                len(equipo) == 3,
                bool(estado_juego.get("avatar"))
            ]
            if all(condiciones):
                self.btn_comenzar.config(state="normal", fg="#2ecc71")
            else:
                self.btn_comenzar.config(state="disabled", fg="gray")

    # --- PANTALLA DE VICTORIA FINAL ---
    def mostrar_victoria_final(self):
        self.limpiar_pantalla_recursiva(self.contenedor.winfo_children())
        
        canvas_v = tk.Canvas(self.contenedor, width=1280, height=720, bg="#0a0a0a", highlightthickness=0)
        canvas_v.pack(fill="both", expand=True)

        # ¡LA SOLUCIÓN AL NOMBRE! Leemos directamente de StringVar de Tkinter
        nombre_raw = self.var_nombre.get().strip()
        nombre_usuario = nombre_raw if len(nombre_raw) > 0 else "Jugador"
        
        # EL SCORE: Aquí leerá lo que tú configures en tu lógica de combate.
        # Si no lo encuentra, mostrará 0 por defecto.
        puntaje_total = estado_juego.get("score", 0)

        # Textos de Victoria
        canvas_v.create_text(640, 150, text="¡SISTEMA LIBERADO!", 
                            font=("Consolas", 50, "bold"), fill="#f1c40f")
        
        canvas_v.create_text(640, 300, text=f"INCREÍBLE TRABAJO, {nombre_usuario.upper()}", 
                            font=("Consolas", 30, "bold"), fill="white")
        
        canvas_v.create_text(640, 420, text=f"PUNTAJE FINAL: {puntaje_total}", 
                            font=("Consolas", 35), fill="#2ecc71")

        btn_salir = tk.Button(
            self.contenedor, 
            text="SALIR AL ESCRITORIO", 
            font=("Consolas", 16, "bold"),
            bg="#c0392b", 
            fg="white",
            padx=30,
            pady=10,
            command=self.root.quit
        )
        canvas_v.create_window(640, 580, window=btn_salir)