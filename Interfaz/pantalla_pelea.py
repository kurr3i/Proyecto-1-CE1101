import tkinter as tk
import sys
import os
from Interfaz.componentes import cargar_img
from Logic.combate import inicializar_batalla, procesar_ataque_recursivo, gestionar_captura
from Logic.datos import db_personajes 
from Logic.motor import registrar_victoria_nivel

def limpiar_recursivo(widgets):
    if not widgets: return
    widgets[0].destroy()
    limpiar_recursivo(widgets[1:])

def reiniciar_juego():
    """Reinicia el proceso completo del juego."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

def crear_pantalla_pelea(frame_padre, estado_juego, callback_regreso, callback_victoria):
    limpiar_recursivo(frame_padre.winfo_children())
    datos = inicializar_batalla(estado_juego["personajes_elegidos"])
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.refs = {}

    # --- FUNCIONES DE APOYO ---
    def obtener_nombre_seguro(pj):
        if not pj: return "Desconocido"
        return pj.get("nombre") or pj.get("name") or pj.get("Nombre") or "Desconocido"

    def mostrar_game_over():
        """Capa visual de derrota."""
        canvas.create_rectangle(0, 0, 1280, 720, fill="black", stipple="gray50", tags="dinamico")
        canvas.create_text(640, 300, text="GAME OVER", font=("Consolas", 80, "bold"), fill="#c0392b", tags="dinamico")
        canvas.create_text(640, 400, text="Tu luchador ha caído. La misión ha fallado.", 
                          font=("Consolas", 20), fill="white", tags="dinamico")
        
        btn_retry = tk.Button(frame_padre, text="REINTENTAR DESDE EL INICIO", font=("Consolas", 14, "bold"),
                             bg="#2ecc71", fg="white", padx=20, pady=10, command=reiniciar_juego)
        canvas.create_window(640, 500, window=btn_retry, tags="dinamico")

    def actualizar_escena_recursiva(lista_bandos):
        # 1. Dibujar el fondo solo una vez (cuando la lista está completa)
        if len(lista_bandos) == 2:
            canvas.delete("dinamico")
            bg = cargar_img("fondo_pelea.png")
            if bg:
                canvas.refs["bg"] = bg
                canvas.create_image(0, 0, image=bg, anchor="nw")

        if not lista_bandos: return

        lado, p = lista_bandos[0]
        if p:
            nombre = obtener_nombre_seguro(p)
            # Posición de las barras de vida
            x_pos = 100 if lado == "jugador" else 780
            
            info_db = db_personajes.get(nombre, {})
            hp_max = info_db.get("hp", 100)
            hp_actual = p.get("hp", 0)
            ratio = (hp_actual / hp_max) if hp_max > 0 else 0
            
            # Dibujar Barras de vida (se mantienen igual)
            canvas.create_rectangle(x_pos, 60, x_pos+400, 85, fill="#c0392b", outline="white", tags="dinamico")
            canvas.create_rectangle(x_pos, 60, x_pos+(400*ratio), 85, fill="#2ecc71", outline="white", tags="dinamico")
            canvas.create_text(x_pos+200, 45, text=f"{nombre}: {hp_actual} HP", 
                               fill="white", font=("Consolas", 12, "bold"), tags="dinamico")

            # --- LÓGICA DE SPRITE (Lado Izquierdo para el Jugador) ---
            # Buscamos el nombre del archivo del sprite
            nombre_sprite = p.get("sprite") 
            
            # Cargamos la imagen desde la carpeta Assets
            sprite_img = cargar_img(nombre_sprite)
            
            if sprite_img:
                # Guardamos la referencia para que Python no la borre de memoria
                canvas.refs[f"spr_{lado}"] = sprite_img
                
                # px = 350 es el lado IZQUIERDO (Jugador)
                # px = 930 es el lado DERECHO (Hollow)
                px = 350 if lado == "jugador" else 930
                py = 450 # Altura en el campo
                
                canvas.create_image(px, py, image=sprite_img, tags="dinamico")

        # Llamada recursiva para procesar al siguiente bando (el enemigo)
        actualizar_escena_recursiva(lista_bandos[1:])

    # --- LÓGICA DE TURNOS ---
    def manejar_ataque():
        btn_atk.config(state="disabled")
        btn_sw.config(state="disabled")
        
        ko, danio_real = procesar_ataque_recursivo(datos, True)
        actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), 
                                    ("hollow", datos.get("activo_hollow"))])
        
        if ko:
            gestionar_captura(datos, False)
            
            # --- EL ARREGLO ESTÁ AQUÍ ---
            if not datos.get("equipo_hollow"): 
                # Subimos el progreso
                estado_juego["progreso"] = estado_juego.get("progreso", 0) + 1
                
                # ¡FALTABA ESTE RETURN! Esto corta la función y nos devuelve a main_window
                return callback_regreso() 
            # ----------------------------
            
            # Si el código llega hasta aquí, significa que SÍ quedan enemigos
            datos["activo_hollow"] = datos["equipo_hollow"][0]
            actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), 
                                        ("hollow", datos.get("activo_hollow"))])
        
        frame_padre.after(1000, turno_enemigo)

    def turno_enemigo():
        if not datos["activo_jugador"]: return # Seguridad si ya murió
        
        ko, _ = procesar_ataque_recursivo(datos, False)
        actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), ("hollow", datos.get("activo_hollow"))])
        
        if ko:
            gestionar_captura(datos, True)
            btn_atk.config(state="disabled")
            btn_sw.config(state="disabled")
            mostrar_game_over() 
        else:
            btn_atk.config(state="normal")
            btn_sw.config(state="normal")

    def generar_botones_recursivo(contenedor, lista_pjs, ventana_ref, es_inicio):
        if not lista_pjs: return
        pj = lista_pjs[0]
        nombre_pj = obtener_nombre_seguro(pj)
        vida_actual = pj.get("hp", 0)
        esta_vivo = vida_actual > 0
        info_db = db_personajes.get(nombre_pj, {})
        img_btn = cargar_img(str(pj.get("img") or info_db.get("img") or "default.png"))

        btn = tk.Button(contenedor, text=f"{nombre_pj.upper()}\nHP: {vida_actual}",
                        image=img_btn, compound="top", width=160, height=200,
                        font=("Consolas", 10, "bold"), bg="#2c3e50" if esta_vivo else "#c0392b",
                        fg="white", state="normal" if esta_vivo else "disabled",
                        command=lambda p=pj: confirmar_seleccion(p, ventana_ref))
        btn.pack(side="left", padx=15)
        btn.image = img_btn 
        generar_botones_recursivo(contenedor, lista_pjs[1:], ventana_ref, es_inicio)

    def abrir_mini_menu_seleccion():
        ventana_sel = tk.Toplevel(frame_padre)
        ventana_sel.title("Selección")
        ventana_sel.geometry("750x350")
        ventana_sel.configure(bg="#0a0a0a")
        ventana_sel.transient(frame_padre)
        ventana_sel.grab_set() 
        
        tk.Label(ventana_sel, text="¿A QUIÉN ENVIARÁS?", font=("Consolas", 16, "bold"), 
                 bg="#0a0a0a", fg="#f1c40f").pack(pady=20)
        frame_opciones = tk.Frame(ventana_sel, bg="#0a0a0a")
        frame_opciones.pack(expand=True)
        generar_botones_recursivo(frame_opciones, datos.get("equipo_jugador", []), ventana_sel, True)

    def confirmar_seleccion(pj_elegido, ventana):
        datos["activo_jugador"] = pj_elegido
        ventana.destroy()
        actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), ("hollow", datos.get("activo_hollow"))])
        btn_atk.config(state="normal")
        btn_sw.config(state="normal")

    # --- ELEMENTOS DE INTERFAZ (BOTONES) ---
    btn_atk = tk.Button(frame_padre, text="ATAQUE", font=("Consolas", 14, "bold"), 
                        bg="#e74c3c", fg="white", width=12, command=manejar_ataque)
    btn_sw = tk.Button(frame_padre, text="CAMBIAR", font=("Consolas", 14, "bold"), 
                       bg="#3498db", fg="white", width=12, command=abrir_mini_menu_seleccion)
    
    canvas.create_window(540, 650, window=btn_atk)
    canvas.create_window(740, 650, window=btn_sw)

    # Iniciar con selección obligatoria
    btn_atk.config(state="disabled")
    btn_sw.config(state="disabled")
    abrir_mini_menu_seleccion()